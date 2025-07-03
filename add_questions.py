import sqlite3
import json
import random

conn = sqlite3.connect("smartquiz.db")
cursor = conn.cursor()

# 50件のサンプル問題（簡単な例題ベースで生成）
sample_data = [
    ("日本の通貨単位は？", ["ドル", "ユーロ", "円", "ポンド"], 2),
    ("水の化学式は？", ["H2O", "CO2", "NaCl", "O2"], 0),
    ("日本の首相公邸がある都市は？", ["大阪", "京都", "東京", "名古屋"], 2),
    ("桜の季節はいつ？", ["春", "夏", "秋", "冬"], 0),
    ("最も長い川は？", ["ナイル川", "アマゾン川", "ミシシッピ川", "黄河"], 1),
    ("野球のボールの縫い目は？", ["赤", "青", "黒", "白"], 0),
    ("りんごは何の果物？", ["根菜", "果物", "穀物", "豆類"], 1),
    ("光の速さは？", ["約30万km/秒", "約10万km/秒", "約5万km/秒", "約1万km/秒"], 0),
    ("日本の祝日でないのは？", ["勤労感謝の日", "文化の日", "読書の日", "建国記念の日"], 2),
    ("太陽は何の星？", ["惑星", "恒星", "衛星", "彗星"], 1),
]

# ランダムに50件生成
questions_to_add = []
for i in range(50):
    base = random.choice(sample_data)
    q_text = f"{base[0]}（No.{i+1}）"
    options = base[1]
    correct = base[2]
    questions_to_add.append((q_text, json.dumps(options, ensure_ascii=False), correct))

# INSERT 実行
cursor.executemany(
    "INSERT INTO questions (question, options, correct_index) VALUES (?, ?, ?)",
    questions_to_add
)

conn.commit()
conn.close()
print("✅ 50件のクイズ問題を smartquiz.db に追加しました。")
