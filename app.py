from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alternatives = db.Column(db.String(255), nullable=False)
    Q = db.Column(db.String(255), nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    explanation = db.Column(db.String(255), nullable=False)
    referTo = db.Column(db.String(255), nullable=False)

    def __init__(self, alternatives, Q, correct, explanation, referTo):
        self.alternatives = alternatives
        self.Q = Q
        self.correct = correct
        self.explanation = explanation
        self.referTo = referTo

@app.route('/questions', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    return jsonify([{"alternatives": q.alternatives, "Q": q.Q, "correct": q.correct, "explanation": q.explanation, "referTo": q.referTo} for q in questions])

@app.route('/questions', methods=['POST'])
def add_question():
    data = request.json
    new_question = Question(data['alternatives'], data['Q'], data['correct'], data['explanation'], data['referTo'])
    db.session.add(new_question)
    db.session.commit()
    return jsonify({"message": "Question added successfully!"})

@app.route('/questions/<int:id>', methods=['PATCH'])
def update_question(id):
    question = Question.query.get(id)
    data = request.json
    question.alternatives = data['alternatives']
    question.Q = data['Q']
    question.correct = data['correct']
    question.explanation = data['explanation']
    question.referTo = data['referTo']
    db.session.commit()
    return jsonify({"message": "Question updated successfully!"})

@app.route('/questions/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)
    db.session.delete(question)
    db.session.commit()
    return jsonify({"message": "Question deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
