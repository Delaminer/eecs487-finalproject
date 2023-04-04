
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

class DataLoader(Dataset):
    def __init__ (self, filepath="../dataset/dataset_subset400.csv", save_name = "saved_data400.pkl"):
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
        self.titles_id = []
        self.unique_titles_id = set()
        
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
                with open("titles_id_"+ save_name, "rb") as f:
                    self.titles_id = pickle.load(f)
                    print("Successfully load titles_id")
                return 
            except Exception as e:
                print("Some errros happened when loading pickle files")
                print(e)
                
        # only loading the titles for now 
        for index, row in df.iterrows():
            
            # for now we are just doing title
            # BUT possibly can try body and stuff in the future 
            encoded_q1 = torch.Tensor(encode_sentence(row["q1_title"]))
            encoded_q2 = torch.Tensor(encode_sentence(row["q2_title"]))
            
            if row["q1_id"] not in self.unique_titles_id:
                self.unique_titles_id.add(row["q1_id"])
                self.unique_titles.append(encoded_q1) # gonna be fed into the KNN algorithm 
                self.titles_id.append(int(row["q1_id"])) # i need to know which question the KNN predicts
                
            if row["q2_id"] not in self.unique_titles_id:
                self.unique_titles_id.add(row["q2_id"])
                self.unique_titles.append(encoded_q2)
                self.titles_id.append(int(row["q2_id"]))
                
                
            # NOTE about the above code ^^^
            # Since we add unique_title and its id at the same order
            # When we call knn, we are able to retrive its real id by 
            # looking at the indexes returned by knn, and then index those 
            # indexes using self.titles_id.
                
            cur_data = {}
            print("Currently processing row", index)
            cur_data["Q1_title"] = encoded_q1
            cur_data["Q1_id"] = int(row["q1_id"])
            cur_data["Q2_title"] = encoded_q2
            cur_data["Q2_id"] = int(row["q2_id"])
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
            with open("titles_id_"+ save_name, "wb") as f:
                pickle.dump(self.titles_id, f)
                print("Successfully wrote titles_id")
                
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
    def __init__(self, new_dimension=64):
        super(FineTunedModel, self).__init__()
        
        input_dimension = 768
        self.relu = nn.ReLU()
        # NOTE: Maybe reduce to 1 layer
        self.do = nn.Dropout(p=0.5)
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
        
