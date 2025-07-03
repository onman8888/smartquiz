import sqlite3
import json
import random

conn = sqlite3.connect("smartquiz.db")
cursor = conn.cursor()

# --- questions テーブルに 10 件追加 ---
new_questions = [
    ("日本の国鳥は？", ["ツル", "キジ", "ハト", "フクロウ"], 1),
    ("元素記号 H は何？", ["ヘリウム", "水素", "酸素", "窒素"], 1),
    ("富士山の高さは？", ["3776m", "2800m", "4000m", "3050m"], 0),
    ("「犬も歩けば」何に当たる？", ["棒", "猫", "壁", "車"], 0),
    ("赤道直下の国はどれ？", ["日本", "エクアドル", "カナダ", "ノルウェー"], 1),
    ("「3の倍数」はどれ？", ["5", "9", "11", "13"], 1),
    ("月の満ち欠けに関係するものは？", ["太陽", "地球", "火星", "木星"], 0),
    ("世界最大の大陸は？", ["アジア", "アフリカ", "南極", "ヨーロッパ"], 0),
    ("九九で8×7は？", ["54", "56", "58", "60"], 1),
    ("円周率（π）は？", ["2.14", "3.14", "4.14", "5.14"], 1)
]

for q in new_questions:
    cursor.execute(
        "INSERT INTO questions (question, options, correct_index) VALUES (?, ?, ?)",
        (q[0], json.dumps(q[1], ensure_ascii=False), q[2])
    )

# --- results テーブルに 10 件追加（ランダムなダミーデータ） ---
cursor.execute("SELECT id FROM questions")
question_ids = [row[0] for row in cursor.fetchall()]

for _ in range(10):
    qid = random.choice(question_ids)
    time = round(random.uniform(2.0, 10.0), 2)
    mistakes = random.randint(0, 3)
    cursor.execute(
        "INSERT INTO results (question_id, time, mistakes) VALUES (?, ?, ?)",
        (qid, time, mistakes)
    )

conn.commit()
conn.close()
print("✅ questions と results テーブルにそれぞれ10件ずつ追加しました。")
