from annoy import AnnoyIndex
from nltk import sent_tokenize
import torch
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text as text

from preprocess_functions import get_question_dict


# Load the Preprocessor and Bert models, this is gonna take a while
# we are loading the version that automatically lowercase the words for us
BERT_URL = "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4"
PREPROCESS_URL = "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
preprocessor = hub.KerasLayer(PREPROCESS_URL)
bert_model =  hub.KerasLayer(BERT_URL)
questions = get_question_dict()

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
    return bert_results["pooled_output"][0]
