import numpy as np
import pickle
import boto3
import boto3.session
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import pandas as pd
import os
import random

ACCESS_KEY = "AKIATB4NJKW5HENP6TE7"
SECRET_KEY = "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"

s3client = boto3.client('s3', 
                        aws_access_key_id = ACCESS_KEY, 
                        aws_secret_access_key = SECRET_KEY
                       )

response = s3client.get_object(Bucket='eecs487-finalproject', Key='question_answer.pkl')

body = response['Body'].read()
question_answers = pickle.loads(body)

def get_answer_for_question(qid):
    if qid in question_answers.keys():
        return question_answers[qid]
    else:
        return None



class TFIDFDataset():
    def __init__ (self, filepath="dataset.csv", testing_split=0):
        save_model = False
        self.data = []
        self.unique_embeddings = []
        self.unique_embeddings_id = []
        self.seen_id = set()
        url = "https://raw.githubusercontent.com/Delaminer/eecs487-finalproject/main/dataset/dataset.csv"
        print("Reading from URL")
        df = pd.read_csv(url)
        print("Done reading from URL")
                
        # self.vectorizer = 
        self.corpus = [] # For TF-IDF, map corpus_id to 
        self.training_corpus = [] # For TF-IDF, map corpus_id to 
        self.id_to_corpus = dict() # map doc_id to corresponding corpus_id
        self.corpus_to_id = dict() # map corpus_id to corresponding doc_id
        self.duplicate = defaultdict(lambda: []) # map doc_id to a duplicate doc_id (very similar questions)
        self.is_doc_testing = {} # Map doc_id to True if in the testing section

        training_count = 0
        testing_count = 0

        # only loading the titles for now 
        for index, row in df.iterrows():
            cur_data = {}
            # print("Currently processing row", index)
            cur_data["q1_text"] = row["q1_title"] # + " " + row["q1_body"]
            cur_data["q1_id"] = int(row["q1_id"])
            cur_data["q2_text"] = row["q2_title"] # + " " + row["q2_body"]
            cur_data["q2_id"] = int(row["q2_id"])
            cur_data["label"] = 1 if int(row["duplicate_label"]) == 1 else -1
            if cur_data["label"] == 1:
                self.duplicate[cur_data["q1_id"]].append(cur_data["q2_id"])
                self.duplicate[cur_data["q2_id"]].append(cur_data["q1_id"])
            self.data.append(cur_data)
            for id, entry in [(cur_data["q1_id"], cur_data["q1_text"]), (cur_data["q2_id"], cur_data["q2_text"])]:
                if id not in self.id_to_corpus:
                    self.id_to_corpus[id] = len(self.corpus) # Map the id to the entry's index in self.corpus
                    self.corpus_to_id[len(self.corpus)] = id # Map the index in self.corpus to the id
                    self.corpus.append(entry)
                    # Assign this to testing or training dataset
                    is_testing = random.random() < testing_split
                    self.is_doc_testing[id] = is_testing
                    if is_testing:
                        testing_count += 1
                    else:
                        self.training_corpus.append(entry)
                        training_count += 1
        emp_testing_split = testing_count / (testing_count + training_count)
        print(f"There are {training_count} training and {testing_count} testing examples. Testing ratio = {emp_testing_split} vs {testing_split}")

        self.vectorizer = TfidfVectorizer()
        self.vectorizer.fit(self.training_corpus)
        self.matrix = self.vectorizer.transform(self.corpus)
        print("Special tfidf dataloader done processing.")
        print("Keep in mind the data processed is in order, so you might want to shuffle them.")
        
    def __len__(self):
        return self.matrix.shape[0]
    
    def __getitem__(self, idx):
        return self.matrix[idx]

