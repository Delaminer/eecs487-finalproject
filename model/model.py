
import numpy as np
import torch
from torch.utils.data import Dataset
import torch.nn as nn
import torch.nn.functional as F
import sys
import os
sys.path.append("..") # need this to import form sibling directory 
print(sys.path)
import pandas as pd
import csv
import pickle
from utils.helper import *
from torch.nn.functional import normalize
import random

class NormalLoader(Dataset):
    def __init__ (self, filepath="../dataset/dataset_subset800.csv", save_name = "saved_data800.pkl"):
        super().__init__()
            
        # Each data point is a pair of embeddings 
        # If the data point is labeled as a dup,
        # then Q1 is the duplicate, and Q2 is the original
        # Else if the data point is labeled as a non-dup, 
        # then Q1 is the duplicate, and Q2 is the random-sampled question
        
        # data is a csv file in the following format
        # Q1 title, Q1 body, Q1 id, Q2 title, Q2 body, Q2 id, dup. label
        self.data = []
        self.unique_titles = []
        self.unique_titles_ids = []
        self.seen_id = set()
        
        tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        # model = BertModel.from_pretrained("bert-base-uncased", return_dict=True)
        # helper function for calculating the inptu and attention_mask 
        def ff(sentence):
                
            encoding = tokenizer([sentence], return_tensors='pt', padding=True, truncation=True)
            input_ids = encoding['input_ids']
            attention_mask = encoding['attention_mask']
            return input_ids, attention_mask
            # return model(input_ids, attention_mask=attention_mask).pooler_output[0]
            
        df = pd.read_csv(filepath) 
        
        if os.path.isfile(save_name):
            print("Found saved data")
            try:
                with open(save_name, "rb") as f:
                    self.data = pickle.load(f)
                    print("Successfully load pickle files")
                with open("unique_embeddings_"+ save_name, "rb") as f:
                    self.unique_embeddings = pickle.load(f)
                    print("Successfully load unique_titles")
                with open("unique_embeddings_id_"+ save_name, "rb") as f:
                    self.unique_embeddings_id = pickle.load(f)
                    print("Successfully load titles_id")
                return 
            except Exception as e:
                print("Some errros happened when loading pickle files")
                print(e)
        # load the data if it was saved before 
        for index, row in df.iterrows():
            
            # for now we are just doing title
            # BUT possibly can try body and stuff in the future
            
            # if this id is not seen before, we add the data point 
            if row["q1_id"] not in self.seen_id:
                self.seen_id.add(row["q1_id"])
                
                # q1_concat = row["q1_title"] + " " + row["q1_body"] 
                # encoded_q1 = torch.Tensor(encode_sentence(q1_concat))
                self.unique_titles_ids.append(int(row["q1_id"]))
                self.unique_titles.append(row["q1_title"]) # gonna be fed into the KNN algorithm 
                                                          # i need to know which question the KNN predicts
                
            if row["q2_id"] not in self.seen_id:
                self.seen_id.add(row["q2_id"])
                
                # q2_concat = row["q2_title"] + " " + row["q2_body"] 
                # encoded_q2 = torch.Tensor(encode_sentence(q2_concat))
                self.unique_titles_ids.append(int(row["q2_id"]))
                self.unique_titles.append(row["q2_title"])
                
                
            # NOTE about the above code ^^^
            # Since we add unique_title and its id at the same order
            # When we call knn, we are able to retrive its real id by 
            # looking at the indexes returned by knn, and then index those 
            # indexes using self.titles_id.
                
            in1, atten1 = ff(row["q1_title"])
            in2, atten2 = ff(row["q2_title"])
            cur_data = {}
            print("Currently processing row", index)
            cur_data["q1_title"] = row["q1_title"]
            cur_data["q1_id"] = int(row["q1_id"])
            cur_data["input1"] = in1
            cur_data["atten1"] = atten1
            cur_data["input2"] = in2
            cur_data["atten2"] = atten2
            cur_data["q2_title"] = row["q2_title"]
            cur_data["q2_id"] = int(row["q2_id"])
            # we need to reformat label to be -1 if it's 0, because CosineEmbeddingLoss 
            # expects y to either be 1 or -1 
            cur_data["label"] = 1 if int(row["duplicate_label"]) == 1 else -1
            
            self.data.append(cur_data)
        try:
            print("Pickling data...")
            
            with open(save_name, "wb") as f:
                pickle.dump(self.data, f)
                print("Successfully wrote data")
            with open("unique_titles_"+ save_name, "wb") as f:
                pickle.dump(self.unique_titles, f)
                print("Successfully wrote unique_titles")
            with open("unique_titles_id_"+ save_name, "wb") as f:
                pickle.dump(self.unique_titles_ids, f)
                print("Successfully wrote unique_titles_id")
                
        except Exception as e:
            print("Some errors happened in pickling data")
            print(e)
            
        print("NormalLoader done processing.")
        print("Keep in mind the data processed is in order, so you might want to shuffle them.")
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]
    
class DataLoader(Dataset):
    def __init__ (self, filepath="../dataset/dataset_subset800.csv", save_name = "saved_data800.pkl"):
        super().__init__()
            
        # Each data point is a pair of embeddings 
        # If the data point is labeled as a dup,
        # then Q1 is the duplicate, and Q2 is the original
        # Else if the data point is labeled as a non-dup, 
        # then Q1 is the duplicate, and Q2 is the random-sampled question
        
        # data is a csv file in the following format
        # Q1 title, Q1 body, Q1 id, Q2 title, Q2 body, Q2 id, dup. label
        self.data = []
        self.unique_embeddings = []
        self.unique_embeddings_id = []
        self.seen_id = set()
        
        df = pd.read_csv(filepath) 
        
        # load the data if it was saved before 
        
        if os.path.isfile(save_name):
            print("Found saved data")
            try:
                with open(save_name, "rb") as f:
                    self.data = pickle.load(f)
                    print("Successfully load pickle files")
                with open("unique_titles_"+ save_name, "rb") as f:
                    self.unique_titles = pickle.load(f)
                    print("Successfully load unique_titles")
                with open("unique_titles_id_"+ save_name, "rb") as f:
                    self.unique_titles_ids = pickle.load(f)
                    print("Successfully load titles_id")
                return 
            except Exception as e:
                print("Some errros happened when loading pickle files")
                print(e)
                
        # only loading the titles for now 
        for index, row in df.iterrows():
            
            # for now we are just doing title
            # BUT possibly can try body and stuff in the future
            
            # if this id is not seen before, we add the data point 
            if row["q1_id"] not in self.seen_id:
                self.seen_id.add(row["q1_id"])
                
                # q1_concat = row["q1_title"] + " " + row["q1_body"] 
                # encoded_q1 = torch.Tensor(encode_sentence(q1_concat))
                encoded_q1 = torch.Tensor(encode_sentence(row["q1_title"]))
                self.unique_embeddings_id.append(int(row["q1_id"]))
                self.unique_embeddings.append(encoded_q1) # gonna be fed into the KNN algorithm 
                                                          # i need to know which question the KNN predicts
                
            if row["q2_id"] not in self.seen_id:
                self.seen_id.add(row["q2_id"])
                
                # q2_concat = row["q2_title"] + " " + row["q2_body"] 
                # encoded_q2 = torch.Tensor(encode_sentence(q2_concat))
                encoded_q2 = torch.Tensor(encode_sentence(row["q2_title"]))
                self.unique_embeddings_id.append(int(row["q2_id"]))
                self.unique_embeddings.append(encoded_q2)
                
                
            # NOTE about the above code ^^^
            # Since we add unique_title and its id at the same order
            # When we call knn, we are able to retrive its real id by 
            # looking at the indexes returned by knn, and then index those 
            # indexes using self.titles_id.
                
            cur_data = {}
            print("Currently processing row", index)
            cur_data["q1_embedding"] = encoded_q1
            cur_data["q1_id"] = int(row["q1_id"])
            cur_data["q2_embedding"] = encoded_q2
            cur_data["q2_id"] = int(row["q2_id"])
            # we need to reformat label to be -1 if it's 0, because CosineEmbeddingLoss 
            # expects y to either be 1 or -1 
            cur_data["label"] = 1 if int(row["duplicate_label"]) == 1 else -1
            
            self.data.append(cur_data)
        
        try:
            print("Pickling data...")
            
            with open(save_name, "wb") as f:
                pickle.dump(self.data, f)
                print("Successfully wrote data")
            with open("unique_embeddings_"+ save_name, "wb") as f:
                pickle.dump(self.unique_embeddings, f)
                print("Successfully wrote unique_embeddings")
            with open("unique_embeddings_id_"+ save_name, "wb") as f:
                pickle.dump(self.unique_embeddings_id, f)
                print("Successfully wrote unique_embeddings_id")
                
        except Exception as e:
            print("Some errors happened in pickling data")
            print(e)
            
        print("Dataloader done processing.")
        print("Keep in mind the data processed is in order, so you might want to shuffle them.")
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]
# this is the model we use to finetune 
class FineTunedModel(nn.Module):
    def __init__(self, new_dimension=64, dropout=0.5):
        super(FineTunedModel, self).__init__()
        
        input_dimension = 768
        self.relu = nn.ReLU()
        # NOTE: Maybe reduce to 1 layer
        self.do = nn.Dropout(p=dropout)
        self.fc1 = nn.Linear(input_dimension, new_dimension)
        self.fc2 = nn.Linear(new_dimension, new_dimension)
        self.fc3 = nn.Linear(new_dimension, new_dimension)
        
    # This is the function to getting the new embedding
    def ff(self, a):
        a = self.fc1(a)
        a = self.relu(a)
        a = self.do(a)
        
        a = self.fc2(a)
        a = self.relu(a)
        a = self.do(a)
        
        a = self.fc3(a)
        # gradient clipping 
        a = normalize(a, dim=0)
        return a 
    
    def forward(self, q1, q2):  
        
        q1 = self.ff(q1)
        q2 = self.ff(q2)
        sim = get_probability(q1.detach(), q2.detach())
        # get the cosine similairty probability between q1 and q2
        return q1, q2, sim
        
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
class SpecialDataLoader(Dataset):
    def __init__ (self, filepath="../dataset/dataset.csv", save_name = "../dataset/tfidf.pkl", testing_split=0):
        super().__init__()
        save_model = False
        self.data = []
        self.unique_embeddings = []
        self.unique_embeddings_id = []
        self.seen_id = set()
        df = pd.read_csv(filepath)         
        if save_model and os.path.isfile(save_name):
            print("Found saved data")
            try:
                with open(save_name, "rb") as f:
                    self.data = pickle.load(f)
                    print("Successfully load pickle files")
                with open("unique_embeddings_"+ save_name, "rb") as f:
                    self.unique_embeddings = pickle.load(f)
                    print("Successfully load unique_titles")
                with open("unique_embeddings_id_"+ save_name, "rb") as f:
                    self.unique_embeddings_id = pickle.load(f)
                    print("Successfully load titles_id")
                return 
            except Exception as e:
                print("Some errros happened when loading pickle files")
                print(e)
                
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
        print("Performed tf-idf")
        if save_model:
            try:
                print("Pickling data...")
                with open(save_name, "wb") as f:
                    pickle.dump(self.data, f)
                    print("Successfully wrote data")    
            except Exception as e:
                print("Some errors happened in pickling data")
                print(e)
            
        print("Special dataloader done processing.")
        print("Keep in mind the data processed is in order, so you might want to shuffle them.")
        
    def __len__(self):
        return self.matrix.shape[0]
    
    def __getitem__(self, idx):
        return self.matrix[idx]

