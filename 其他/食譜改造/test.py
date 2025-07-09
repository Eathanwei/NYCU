import pickle
from sklearn.metrics.pairwise import cosine_similarity
import requests
import re
import ast
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# === Groq 設定 ===
GROQ_API_KEY = "gsk_"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def call_groq(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# === 載入模型與資料 ===
with open("model.pkl", "rb") as f:
    df, tfidf_matrix, vectorizer = pickle.load(f)

def format_steps_as_numbered_line(step_list):
    return " ".join([f"{i+1}. {step}" for i, step in enumerate(step_list)])

# === 顯示 recipe ===
def display_recipe(result):
    print(f"\n🍽️ Title：{result['title']}\n")
    print("📋Ingredients")
    for item in result["ingredients"]:
        print(f"- {item}")
    print("\n📝 Directions：")
    # 修復雙雙引號 → 單雙引號
    clean = result["directions"].replace('""', '"')
    # 轉成真正的 list
    steps = ast.literal_eval(clean)
    # 編號輸出
    for i, step in enumerate(steps, 1):
        print(f"{i}. {step}")

# === 搜尋功能（Top 5 + Groq rerank）===
def search_recipe(title, ingredients, weight):
    query = (title + " ") * int(weight) + " ".join(ingredients)
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-5:][::-1]

    print("\n🔍Top 5 Similar Recipes：")
    options = []
    for i, idx in enumerate(top_indices, 1):
        row = df.iloc[idx]
        name = row["title"]
        ings = ", ".join(row["ingredients"])
        print(f"{i}. {name} | Ingredients：{ings}")
        options.append(f"{i}. {name}: {ings}")

    # Groq 語意選擇最佳
    prompt = (
        f"User is searching for: {title}, ingredients: {', '.join(ingredients)}\n\n"
        "Here are the most similar recipes. Please choose the most relevant one by number only:\n\n" +
        "\n".join(options)
    )
    choice_text = call_groq(prompt)
    match = re.search(r"\d+", choice_text)
    chosen = int(match.group()) if match else 1
    return df.iloc[top_indices[chosen - 1]]

# === 修改建議功能 ===
def modify_ingredients(original_ingredients, requirement):
    prompt = (
        f"Here are the original ingredients: {', '.join(original_ingredients)}.\n"
        f"Please modify them according to this requirement: {requirement}.\n"
        f"Only return the new ingredient list."
    )
    return call_groq(prompt)

def modify_recipe(recipe, requirement):
    prompt = f"""
Original Recipe:

[Title]
{recipe['title']}

[Ingredients]
{chr(10).join(['- ' + ing for ing in recipe['ingredients']])}

[Directions]
{chr(10).join([f"{i+1}. {step}" for i, step in enumerate(ast.literal_eval(recipe['directions']))])}

---

Please rewrite this recipe according to the following requirement:
- Adjust or replace ingredients
- Rewrite steps to match new ingredients
- Rename the recipe if needed

Requirement: {requirement}

Please output in the following format (no explanation, just the content):
[title] New Recipe Title  
[ingredients] (one per line)  
[directions] (one per step)
"""
    reply = call_groq(prompt)
    return reply

always_plural = {
    "noodles", "spaghetti", "greens", "beans", "oats", "cookies", "sprouts", "lentils", "fries", "chips"
}
def normalize_ingredient(text):
    # 將數量與單位去掉，只保留食材名稱
    text = text.lower()
    text = re.sub(r"^[\d/]+(?:\s*[a-z\.]+)?\s+", "", text)  # 例如去掉 "1 cup "
    text = re.sub(r"[^\w\s]", "", text)  # 去除標點符號
    tokens = text.strip().split()
    # 擷取最後一個單字（通常是主要食材名稱），並還原為單數型態
    if not tokens:
        return ""
    last = tokens[-1]
    # 如果在常見複數名詞中，保留原樣
    if last in always_plural:
        return last
    else:
        return lemmatizer.lemmatize(last)

def recommend_from_fridge(fridge_ingredients, weight):
    common_ingredients = {
        "salt", "pepper", "oil", "water", "butter", "sugar", "flour", "garlic", "onion",
        "baking soda", "baking powder", "milk", "egg", "eggs", "soy sauce", "vinegar"
    }

    input_set = set(normalize_ingredient(i) for i in fridge_ingredients)
    def calculate_score(ingredients):
        ing_set = set(normalize_ingredient(i) for i in ingredients if isinstance(i, str))
        if not ing_set:
            return 0
        total = len(ing_set)
        match_user = len(ing_set & input_set)
        match_pantry = len(ing_set & common_ingredients)
        if not ing_set.issubset(input_set | common_ingredients):
            return 0
        if match_user < 2:
            return 0
        score = (match_user * int(weight) + match_pantry * 1) / total
        return score


    df["score"] = df["ingredients"].apply(calculate_score)
    matched_df = df[df["score"] > 0].copy()
    matched_df = matched_df.sort_values("score", ascending=False).head(5)

    if matched_df.empty:
        print("\n❌ No suitable recipes found.")
        return None

    print("\n🧊 These recipes match best with your fridge ingredients:")
    options = []
    for i, (_, row) in enumerate(matched_df.iterrows(), 1):
        name = row["title"]
        ings = ", ".join(row["ingredients"])
        print(f"{i}. {name} | Ingredients: {ings}")
        options.append(f"{i}. {name}: {ings}")

    # 使用 Groq rerank
    prompt = (
        f"Fridge contents: {', '.join(fridge_ingredients)} (pantry items included)\n\n"
        "Choose the best matching recipe by number only:\n\n" + "\n".join(options)
    )
    choice_text = call_groq(prompt)
    match = re.search(r"\d+", choice_text)
    chosen = int(match.group()) if match else 1
    return matched_df.iloc[chosen - 1]

if __name__ == "__main__":
    print("Choose a mode:")
    print("1. search (Find recipe by title and ingredients)")
    print("2. modify (Modify a given ingredient list based on your needs)")
    print("3. fridge (Recommend recipes using only your fridge ingredients)")

    mode_input = input("Enter number or mode name (1. search / 2. modify / 3. fridge): ").strip().lower()
    mode_map = {
        "1": "search",
        "2": "modify",
        "3": "fridge"
    }
    mode = mode_map.get(mode_input, mode_input)

    if mode == "search":
        title = input("Enter recipe title: ")
        ingredients = input("Enter ingredients (comma-separated): ").split(",")
        weight = input("Enter title_weight: ")
        result = search_recipe(title, ingredients, weight)
        print("\n✅ Best matched recipe:")
        display_recipe(result)

        while True:
            choice = input("\nDo you want to modify this recipe based on a requirement? (yes/no): ").strip().lower()
            if choice == "yes":
                requirement = input("Enter your requirement (e.g., vegetarian, gluten-free, high protein): ")
                new_recipe = modify_recipe(result, requirement)
                print("\n📖 Modified Recipe:\n")
                print(new_recipe)
            elif choice == "no":
                print("\n✔️ Search and modify process complete.")
                break
            else:
                print("❌ Please enter yes or no.")

    elif mode == "fridge":
        ingredients = input("Enter ingredients in your fridge (comma-separated): ").split(",")
        weight = input("Enter input_weight: ")
        result = recommend_from_fridge(ingredients, weight)
        if result is not None:
            print("\n✅ Best matched recipe:")
            display_recipe(result)

            while True:
                choice = input("\nDo you want to modify this recipe based on a requirement? (yes/no): ").strip().lower()
                if choice == "yes":
                    requirement = input("Enter your requirement (e.g., vegetarian, gluten-free, high protein): ")
                    new_recipe = modify_recipe(result, requirement)
                    print("\n📖 Modified Recipe:\n")
                    print(new_recipe)
                elif choice == "no":
                    print("\n✔️ Fridge recommendation complete.")
                    break
                else:
                    print("❌ Please enter yes or no.")

    elif mode == "modify":
        original_ingredients = input("Original ingredients (comma-separated): ").split(",")
        requirement = input("Enter requirement (e.g., vegetarian, low sugar, keto): ")
        new_ingredients = modify_ingredients(original_ingredients, requirement)
        print("\n🛠️ Updated Ingredient List:")
        print(new_ingredients)

    else:
        print("❌ Invalid mode. Please enter 1, 2, 3 or one of: search / modify / fridge")
