import numpy as np
import torch
from xml.etree.ElementTree import ElementTree

DATA_PATH = "data\\Posts.xml"

"""
STEPS:
1) Loop through every single post in Posts.xml
2) Get the Question and Title, concatenate them and embed them using BERT
3) Put the embedding into Annoy
"""

"""
Description of the schema:
1) PostTypeID
- 1 -> A question
- 2 -> A answer 
The other values are not important
2) AcceptedAnswerId (only present if PostTypeId = 1)
3) ParentId (only present if PostTypeId = 2, if post is an answer)
4) Scores 
- The score of each post (don't want to use negative scores for answers) 
- But we want to train on negative questions 
5) Body 
- Texts of the question or answer
6) Title
- Might be useful
7) Tags 
- Might be useful 
8) AnswerCount 
9) FavoriteCount 
- Might be useful too 
"""

"""
Put all the embeddings of the question in Annoy 

- Incorporate both the body and title and tags into Annoy

Duplicated flag -> might help here -> might be able to use this for "ground truth"

"""

"""
Find the Xs and ys 

1) Xs -> question 
2) ys -> list of answers (at least 1)

Goal: maximize the cosine simlarity between questions that 
      are similar and minimize questions that are dissimilar

Fine tune process (rough draft):

Input: Will be the BERT embedding(s) of the questions 

Evaluating on: 
"""


tree = ElementTree()
tree.parse("data/Posts.xtml")
posts = list(tree.find("posts").iter("row"))

questions = [
]

for post in posts:
      print(post)
      this_post = {
            "id": post.attrib["Id"],
      }