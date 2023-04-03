
import numpy as np
import torch
from torch.utils.data import Dataset
import torch.nn as nn
import torch.nn.functional as F
from helper import encode_sentence

class MyDataset(Dataset):
    def __init__ (self, data):
        super().__init__()
        self.data = []
        num_entries = len(data)
        print("Entries: ",num_entries)
        i = 0
        for index, entry in data.iterrows():
            if i % 10 == 0:
                print(i)
            i += 1
            q1_embedded = encode_sentence(entry["q1_title"])
            q2_embedded = encode_sentence(entry["q2_title"])
            q1_embedded = torch.from_numpy(q1_embedded.numpy())
            q2_embedded = torch.from_numpy(q2_embedded.numpy())
            X = torch.cat((q1_embedded, q2_embedded), dim=0)
            y = torch.tensor([entry["duplicate_label"]])
            # if y == 1:
            #     y = torch.tensor([0, 1])
            # else:
            #     y = torch.tensor([1, 0])
            datapoint = {
                "X": X,
                "y": y
            }
            self.data.append(datapoint)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]["X"], self.data[idx]["y"]

class MyModel(nn.Module):
    def __init__(self):
        super(MyModel, self).__init__()
        x_dim = 768*2
        self.fc1 = nn.Linear(x_dim, 50)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(50, 1)
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        return x