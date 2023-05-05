from flask import Flask, request, jsonify
import sqlite3
import random

app = Flask(__name__)
DATABASE = 'quiz.db'


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alternatives TEXT,
                question_text TEXT,
                correct INTEGER,
                explanation TEXT,
                refer_to TEXT,
                subject TEXT,
                year INTEGER,
                topic TEXT
            );
        """)


@app.route('/quiz', methods=['POST'])
def add_question():
    data = request.json
    alternatives = data.get('alternatives')
    alternatives_str = ",".join(alternatives)
    question_text = data.get('question_text')
    correct = data.get('correct')
    explanation = data.get('explanation')
    refer_to = data.get('refer_to')
    subject = data.get('subject')
    year = data.get('year')
    topic = data.get('topic')

    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.execute("""
                INSERT INTO quiz (alternatives, question_text, correct, explanation, refer_to, subject, year, topic)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (alternatives_str, question_text, correct, explanation, refer_to, subject, year, topic))
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'Question added successfully'}), 201

@app.route('/quiz', methods=['GET'])
def get_questions():
    subject = request.args.get('subject')
    year = request.args.get('year')
    topic = request.args.get('topic')
    randomize = request.args.get('random') == 'true'

    with sqlite3.connect(DATABASE) as conn:
        if subject and year and topic:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM quiz WHERE subject = ? AND year = ? AND topic = ?;
            """, (subject, year, topic))
        elif subject and topic:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM quiz WHERE subject = ? AND topic = ?;
            """, (subject, topic))
        elif year and topic:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM quiz WHERE year = ? AND topic = ?;
            """, (year, topic))
        elif subject and year:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM quiz WHERE subject = ? AND year = ?;
            """, (subject, year))
        elif subject:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM quiz WHERE subject = ?;
            """, (subject,))
        elif year:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM quiz WHERE year = ?;
            """, (year,))
        elif topic:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM quiz WHERE topic = ?;
            """, (topic,))
        else:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM quiz;
            """)
        data = cursor.fetchall()

    questions = []
    for row in data:
        question = {
            'id': row[0],
            'alternatives': row[1].split(","),
            'question_text': row[2],
            'correct': row[3],
            'explanation': row[4],
            'refer_to': row[5],
            'subject': row[6],
            'year': row[7],
            'topic': row[8]
        }
        questions.append(question)

    if randomize:
        random.shuffle(questions)

    return jsonify(questions)


@app.route('/quiz/<int:id>', methods=['DELETE'])
def delete_question(id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM quiz WHERE id = ?', (id,))
        question = cursor.fetchone()
        if question is None:
            return jsonify({'error': 'Question not found'}), 404
        conn.execute('DELETE FROM quiz WHERE id = ?', (id,))
        conn.commit()

    return jsonify({'message': 'Question deleted'})

@app.route('/quiz/<int:id>', methods=['PATCH'])
def update_question(id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM quiz WHERE id = ?', (id,))
        question = cursor.fetchone()
        if question is None:
            return jsonify({'error': 'Question not found'}), 404

        data = request.json
        alternatives = data.get('alternatives')
        if alternatives:
            alternatives_str = ",".join(alternatives)
            conn.execute('UPDATE quiz SET alternatives = ? WHERE id = ?', (alternatives_str, id))

        question_text = data.get('question_text')
        if question_text:
            conn.execute('UPDATE quiz SET question_text = ? WHERE id = ?', (question_text, id))

        correct = data.get('correct')
        if correct:
            conn.execute('UPDATE quiz SET correct = ? WHERE id = ?', (correct, id))

        explanation = data.get('explanation')
        if explanation:
            conn.execute('UPDATE quiz SET explanation = ? WHERE id = ?', (explanation, id))

        refer_to = data.get('refer_to')
        if refer_to:
            conn.execute('UPDATE quiz SET refer_to = ? WHERE id = ?', (refer_to, id))

        subject = data.get('subject')
        if subject:
            conn.execute('UPDATE quiz SET subject = ? WHERE id = ?', (subject, id))

        year = data.get('year')
        if year:
            conn.execute('UPDATE quiz SET year = ? WHERE id = ?', (year, id))

        topic = data.get('topic')
        if topic:
            conn.execute('UPDATE quiz SET topic = ? WHERE id = ?', (topic, id))

        conn.commit()

    return jsonify({'message': 'Question updated successfully'}), 200
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
