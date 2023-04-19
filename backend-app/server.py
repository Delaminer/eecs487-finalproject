from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from server_helper import get_answer_for_question, TFIDFDataset
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

dataloader = TFIDFDataset()

def get_nearest_questions(text, n=5):
    row = dataloader.vectorizer.transform([text])
    cos_similarities = cosine_similarity(row, dataloader.matrix)
    similar_corpus_indices = cos_similarities.argsort()[0][::-1]
    top_corpus = similar_corpus_indices[:n]
    top_responses = [(dataloader.corpus_to_id[c], dataloader.corpus[c]) for c in top_corpus]
    return top_responses

@app.route('/', methods=['GET'])
def default_page():
    return "Welcome to the backend."


@app.route('/ask', methods=['POST'])
def ask_question():
    data = json.loads(request.get_json())
    question = data['title']
    dup_questions = get_nearest_questions(question, n=5)
    print(f"Got question, {question}, see [{dup_questions[0][0]}] {dup_questions[0][1]}")
    # questions_formatted = [{"id": id, \
    #                         "title": question, \
    #                         "body": get_answer_for_question(id)["question_body"],\
    #                         "answer_id": get_answer_for_question(id)["answer_id"], \
    #                         "answer_body": get_answer_for_question(id)["answer"]} for id, question in dup_questions]
    
    questions_formatted = []
    for id, question in dup_questions:
        cur_answer = get_answer_for_question(id) 
        body = cur_answer["question_body"] if cur_answer != None else None
        answer_id = cur_answer["answer_id"] if cur_answer != None else None
        answer_body = cur_answer["answer"] if cur_answer != None else None
        questions_formatted.append({"id": id, "title": question, "body": body, "answer_id": answer_id, "answer_body": answer_body})
    
    return jsonify({'dup': dup_questions[0][1], "dup_id": dup_questions[0][0], "results": questions_formatted})

if __name__ == '__main__':
    print("Starting server!")
    app.run(debug=False)