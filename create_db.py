import sqlite3

conn = sqlite3.connect("smartquiz.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS results;

CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    options TEXT NOT NULL,
    correct_index INTEGER NOT NULL
);

CREATE TABLE results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    time REAL NOT NULL,
    mistakes INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO questions (question, options, correct_index) VALUES
(
    '日本の首都はどこですか？',
    '["大阪", "札幌", "東京", "福岡"]',
    2
),
(
    '1+1は？',
    '["1", "2", "3", "4"]',
    1
),
(
    'HTMLの略は？',
    '["HyperText Makeup Language", "HyperText Markdown Language", "HyperText Markup Language", "HyperTool Multi Language"]',
    2
);
""")

conn.commit()
conn.close()
print("✅ smartquiz.db が作成されました。")
