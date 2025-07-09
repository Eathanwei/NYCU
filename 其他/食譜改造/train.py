import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import ast

# 讀取資料
df = pd.read_csv("full_dataset.csv")

# 處理 list 欄位（ingredients、NER、directions）
def clean_list_column(s):
    if isinstance(s, str):
        s = s.replace('""', '"')  # 修正 CSV 雙引號
        try:
            return ast.literal_eval(s)
        except:
            return []
    return s if isinstance(s, list) else []

# 清理欄位
df["title"] = df["title"].fillna("").astype(str)
df["ingredients"] = df["ingredients"].apply(clean_list_column)

# 合併欄位供 TF-IDF 使用（強化 title 權重）
df["combined"] = df.apply(
    lambda row: (row["title"] + " ") * 10 + " ".join(row["ingredients"]),
    axis=1
)

# 建立 TF-IDF 模型
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df["combined"])

# 儲存模型
with open("model.pkl", "wb") as f:
    pickle.dump((df, tfidf_matrix, vectorizer), f)

print("✅ 模型訓練完成並已儲存")
