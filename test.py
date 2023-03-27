import tensorflow_hub as hub
import tensorflow as tf
import tensorflow_text as text

# Load the Preprocessor and Bert models, this is gonna take a while
BERT_URL = "https://tfhub.dev/tensorflow/bert_en_uncased_L-12_H-768_A-12/4"
PREPROCESS_URL = "https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/3"
preprocessor = hub.KerasLayer(PREPROCESS_URL)
# text_test = ['this is such an amazing movie!']
# text_preprocessed = preprocessor(text_test)
bert_model =  hub.KerasLayer(BERT_URL)# Testing the embedding 
text_test = ['this is such an amazing movie!', "asdasdasd, asdasd"]

text_preprocessed = preprocessor(text_test)
bert_results = bert_model(text_preprocessed)
    

print(f'Pooled Outputs Shape:{bert_results["pooled_output"].shape}')
print(f'Pooled Outputs Values:{bert_results["pooled_output"][0, :12]}')
print(f'Sequence Outputs Shape:{bert_results["sequence_output"].shape}')
print(f'Sequence Outputs Values:{bert_results["sequence_output"][0, :12]}')
from annoy import AnnoyIndex
# documentation: https://github.com/spotify/annoy
import random
import numpy as np
import torch
import tensorflow_hub as tfh
from xml.etree.ElementTree import ElementTree

tree = ElementTree()
tree.parse("data//Posts.xml")
root = tree.getroot()
posts = root.iter("row")

questions = dict()
answers = dict()
# first preprocess the data and split them into questions and answers
for post in posts:
      if int(post.attrib["PostTypeId"]) == 1:
            if "AnswerCount" in post.attrib and int(post.attrib["AnswerCount"]) > 0:
                  # question
                  this_question = {
                        "id": post.attrib["Id"],
                        "title": post.attrib["Title"],
                        "body": post.attrib["Body"],
                        "accepted": post.attrib["AcceptedAnswerId"] if "AcceptedAnswerId" in post.attrib else -1  
                  }
                  questions[post.attrib["Id"]] = this_question
      elif int(post.attrib["PostTypeId"]) == 2:
            # answer
            this_answer = {
                  "id": post.attrib["Id"],
                  "question_id": post.attrib["ParentId"],
                  "body": post.attrib["Body"],
            }
            answers[post.attrib["Id"]] = this_answer

# print(questions)
# print(answers)

print(f"There are {len(questions)} questions and {len(answers)} answers")
# helper function for encoding a sentence into bert embedding
def encode_sentence(sentence):
    text_preprocessed = preprocessor([sentence])
    bert_results = bert_model(text_preprocessed)
    return bert_results["pooled_output"][0]

# 768 because that's the dimension of bert 
f = 768
assert(encode_sentence("This is a test sentence").shape == 768)
t = AnnoyIndex(f, 'angular')
t.set_seed(487)
for i, word in enumerate(questions.values()):
    v = encode_sentence(word["body"])
    print(i)
    t.add_item(i, v)