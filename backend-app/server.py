from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

import sys 
sys.path.append('../model')
from model import SpecialDataLoader
from sklearn.metrics.pairwise import cosine_similarity
dataloader = SpecialDataLoader(filepath="../dataset/dataset.csv", save_name="../dataset/")
def get_nearest_questions(text, n=5):
    row = dataloader.vectorizer.transform([text])
    cos_similarities = cosine_similarity(row, dataloader.matrix)
    similar_corpus_indices = cos_similarities.argsort()[0][::-1]
    top_corpus = similar_corpus_indices[:n]
    top_responses = [(dataloader.corpus_to_id[c], dataloader.corpus[c]) for c in top_corpus]
    return top_responses


# @app.route('/questions', methods=['GET'])
# def get_questions():
#     return jsonify(questions)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = json.loads(request.get_json())
    question = data['title']
    dup_questions = get_nearest_questions(question, n=5)
    print(f"Got question, {question}, see [{dup_questions[0][0]}] {dup_questions[0][1]}")
    questions_formatted = [{"id": id, "title": question, "body": "unkown"} for id, question in dup_questions]
    return jsonify({'dup': dup_questions[0][1], "dup_id": dup_questions[0][0], "results": questions_formatted})

if __name__ == '__main__':
    print("Starting server!")
    app.run(debug=True, port=5000)
