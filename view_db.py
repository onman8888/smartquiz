import sqlite3
import json

conn = sqlite3.connect("smartquiz.db")
cursor = conn.cursor()

print("\n=== 📝 questions テーブル ===")
cursor.execute("SELECT * FROM questions")
questions = cursor.fetchall()
for q in questions:
    q_id, question, options, correct = q
    print(f"ID: {q_id}\nQ: {question}\n選択肢: {json.loads(options)}\n正解: {correct}\n---")

print("\n=== 🧾 results テーブル ===")
cursor.execute("SELECT * FROM results")
results = cursor.fetchall()
for r in results:
    r_id, q_id, time, mistakes, created = r
    print(f"ID: {r_id} | 問題ID: {q_id} | 時間: {time}秒 | ミス: {mistakes}回 | 登録日時: {created}")

conn.close()
