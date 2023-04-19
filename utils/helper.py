# from annoy import AnnoyIndex
from nltk import sent_tokenize
import torch
import numpy as np
# import tensorflow_hub as hub
# import tensorflow as tf
# import tensorflow_text as text
from utils.preprocess_functions import get_question_dict_no_answer, get_accepted_answers, get_question_answer_dict
# import torch.nn as nn
# m = nn.Sigmoid()

# Load the Preprocessor and Bert models, this is gonna take a while
# we are loading the version that automatically lowercase the words for us
# BERT_URL = "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4"
# PREPROCESS_URL = "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
# preprocessor = hub.KerasLayer(PREPROCESS_URL)
# bert_model =  hub.KerasLayer(BERT_URL)
# preprocessor.save("preprocessor")
# bert_model.save("bert_model")
# import pickle

# with open("preprocessor.pkl", "wb") as f:
#     pickle.dump(preprocessor, f)
#     print("Successfully wrote")
# with open("bert_model.pkl", "wb") as f:
#     pickle.dump(bert_model, f)
#     print("Successfully wrote")
# questions = get_question_dict_no_answer()
# answers = get_accepted_answers()
# question_answers = get_question_answer_dict(questions, answers)

# import pickle

# with open("question_answer.pkl", "wb") as f:
#     pickle.dump(question_answers, f)
#     print("Successfully wrote")
    
import pickle
import boto3
import boto3.session
from dotenv import load_dotenv
import os
load_dotenv()
ACCESS_KEY = os.environ.get("ACCESS_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
s3client = boto3.client('s3', 
                        aws_access_key_id = ACCESS_KEY, 
                        aws_secret_access_key = SECRET_KEY
                       )

response = s3client.get_object(Bucket='eecs487-finalproject', Key='question_answer.pkl')

body = response['Body'].read()
question_answers = pickle.loads(body)


def get_probability(a, b):
    cos_sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    cos_sim = torch.tensor(cos_sim)
    return m(cos_sim)

def get_question_body_from_id(q_id):
    return questions[q_id]["body"]

#feature choice will either be "title" or "body", but we can add a "both" option later
def get_all_question_embeddings(feature_choice="body"):
    #embeddings will be array of shape [num_questions, 2], where each row will be: [question_id, question_embedding]
    embeddings = np.empty([len(questions), 2], dtype=object)

    print("STARTING")

    index = 0
    for id, value in questions.items():
        print(index)
        question_vec = get_paragraph_embedding_bert(value[feature_choice])
        #embeddings[index] = float(id)
        embeddings[index] = [id, question_vec]
        index += 1
    return embeddings

#returns average sentence embedding for given text
def get_paragraph_embedding_bert(text):
    text_preprocessed = preprocessor(sent_tokenize(text))
    bert_results = bert_model(text_preprocessed)
    return np.mean(bert_results["pooled_output"], axis=0)

def encode_sentence(sentence):
    text_preprocessed = preprocessor([sentence])
    bert_results = bert_model(text_preprocessed)
    return np.array(bert_results["pooled_output"][0])

def get_answer_for_question(qid):
    if qid in question_answers.keys():
        return question_answers[qid]
    else:
        return None
