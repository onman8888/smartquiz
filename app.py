from flask import Flask, render_template, jsonify, request
import sqlite3
import json
import random

app = Flask(__name__)

# ---------------------------------
# トップページ（クイズ画面）
# ---------------------------------
@app.route("/")
def index():
    return render_template("quiz.html")

# ---------------------------------
# クイズ問題を取得するAPI
# ---------------------------------
@app.route("/api/questions")
def get_questions():
    print("[INFO] /api/questions にアクセスされました")
    conn = sqlite3.connect("smartquiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, options, correct_index FROM questions")
    rows = cursor.fetchall()
    conn.close()

    questions = []
    for row in rows:
        questions.append({
            "id": row[0],
            "question": row[1],
            "options": json.loads(row[2]),
            "correct": row[3]
        })

    return jsonify(questions)

# ---------------------------------
# 回答結果を保存するAPI
# ---------------------------------
@app.route("/api/submit", methods=["POST"])
def submit_result():
    data = request.get_json()
    print(f"[INFO] /api/submit にPOSTされました: {data}")
    conn = sqlite3.connect("smartquiz.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO results (question_id, time, mistakes) VALUES (?, ?, ?)",
        (data["question_id"], data["time"], data["mistakes"])
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

# ---------------------------------
# 1問だけランダムにWebページで表示
# ---------------------------------
@app.route("/sample-question")
def sample_question():
    print("[INFO] /sample-question にアクセスされました")
    conn = sqlite3.connect("smartquiz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, options, correct_index FROM questions ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        question_data = {
            "id": row[0],
            "question": row[1],
            "options": json.loads(row[2]),
            "correct": row[3]
        }
        print(f"[DATA] 問題ID: {row[0]}, 正解: {row[3]}")
    else:
        print("[ERROR] 問題が取得できませんでした。")
        question_data = None

    return render_template("sample.html", question=question_data)

# ---------------------------------
# 本番環境では app.run() は使いません（Render用）
# ---------------------------------
# if __name__ == "__main__":
#     print("🚀 Flaskアプリを起動中... http://127.0.0.1:5000")
#     app.run(debug=True)
