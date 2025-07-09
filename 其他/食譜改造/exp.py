import pandas as pd
from test import search_recipe, recommend_from_fridge, modify_ingredients, modify_recipe

INPUT_FILE = "recipe_experiment_input.csv"

# 1. Title 權重實驗
def experiment_title_weight():
    df = pd.read_csv(INPUT_FILE)
    results = []
    for i, row in df.iterrows():
        print(i)
        title = row["title"]
        ingredients = row["ingredients"].split(", ")
        for weight in [1, 3, 5, 10, 15, 20]:
            result = search_recipe(title, ingredients, weight)
            results.append({
                "title": title,
                "ingredients": ", ".join(ingredients),
                "weight": weight,
                "recommended_title": result["title"] if result is not None else "N/A"
            })
    pd.DataFrame(results).to_csv("search_results.csv", index=False)
    print("✅ 實驗 1 完成：search_results.csv")

# 2. Fridge 模式實驗
def experiment_fridge_mode():
    df = pd.read_csv(INPUT_FILE)
    results = []
    for i, row in df.iterrows():
        print(i)
        ingredients = row["ingredients"].split(", ")
        for weight in [1, 3, 5, 7, 10]:
            result = recommend_from_fridge(ingredients, weight)
            results.append({
                "ingredients": ", ".join(ingredients),
                "weight": weight,
                "recommended_title": result["title"] if result is not None else "N/A"
            })
    pd.DataFrame(results).to_csv("fridge_results.csv", index=False)
    print("✅ 實驗 2 完成：fridge_results.csv")

# 3. 食材修改實驗
def experiment_ingredient_modify():
    df = pd.read_csv(INPUT_FILE)
    results = []
    for i, row in df.iterrows():
        print(i)
        ingredients = row["ingredients"].split(", ")
        requirement = row["ingredient_change_request"]
        output = modify_ingredients(ingredients, requirement)
        results.append({
            "original_ingredients": ", ".join(ingredients),
            "requirement": requirement,
            "modified_ingredients": output
        })
    pd.DataFrame(results).to_csv("ingredient_modify_results.csv", index=False)
    print("✅ 實驗 3 完成：ingredient_modify_results.csv")

# 4. 食譜完整改寫實驗
def experiment_full_recipe_modify():
    df = pd.read_csv(INPUT_FILE)
    results = []

    for i, row in df.iterrows():
        title = row["title"]
        ingredients = row["ingredients"].split(", ")
        requirement = row["recipe_change_request"]

        # Step 1: search 最相近食譜
        matched_recipe = search_recipe(title, ingredients)

        # Step 2: 用 matched_recipe 和 requirement 改寫整體食譜
        if matched_recipe is not None:
            recipe_obj = {
                "title": matched_recipe["title"],
                "ingredients": matched_recipe["ingredients"],
                "directions": matched_recipe["directions"] if "directions" in matched_recipe else ""
            }
            rewritten = modify_recipe(recipe_obj, requirement)
        else:
            rewritten = "N/A"

        results.append({
            "original_title": title,
            "matched_title": matched_recipe["title"] if matched_recipe is not None else "N/A",
            "requirement": requirement,
            "rewritten_recipe": rewritten
        })

    pd.DataFrame(results).to_csv("full_recipe_rewrites.csv", index=False)
    print("✅ 實驗 4 完成：full_recipe_rewrites.csv")


# === 主程式 ===
if __name__ == "__main__":
    experiment_title_weight()
    experiment_fridge_mode()
    experiment_ingredient_modify()
    experiment_full_recipe_modify()
