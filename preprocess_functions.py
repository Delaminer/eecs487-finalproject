from collections import defaultdict
import numpy as np
import torch
import tensorflow_hub as tfh
from bs4 import BeautifulSoup as bs
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




def get_question_dict_no_answer():
      tree = ElementTree()
      tree.parse("data//Posts.xml")
      root = tree.getroot()
      posts = root.iter("row")

      questions = {}
      # first preprocess the data and split them into questions and answers
      for post in posts:
            if int(post.attrib["PostTypeId"]) == 1:
                  if "AnswerCount" in post.attrib:
                        # question
                        this_question = {
                              "id": int(post.attrib["Id"]),
                              "title": post.attrib["Title"],
                              "body": post.attrib["Body"],
                              "accepted": post.attrib["AcceptedAnswerId"] if "AcceptedAnswerId" in post.attrib else -1  
                        }
                        questions[int(post.attrib["Id"])] = this_question

      # first question
      for id, value in questions.items():
            value["title"] = bs(value["title"], "lxml").text
            value["body"] = bs(value["body"], "lxml").text
            questions[id] = value
      # then answer
      # for id, value in answers.items():
      #       value["body"] = bs(value["body"], "lxml").text
      #       answers[id] = value

      return questions
# tree = ElementTree()
# tree.parse("data//Posts.xml")
# root = tree.getroot()
# posts = root.iter("row")

# questions = dict()
# answers = dict()

# for post in posts:
#       # print(post)
#       # this_post = {
#       #       "id": post.attrib["Id"],
#       #       "post_type": post.attrib["PostTypeId"],
#       #       "title": post.attrib["Title"],
#       #       "body": post.attrib["Body"],
#       #       "accepted": post.attrib["AcceptedAnswerId"] # might be null
#       # }
#       # it's a question
#       if int(post.attrib["PostTypeId"]) == 1:
#             if "AnswerCount" in post.attrib and int(post.attrib["AnswerCount"]) > 0:
#                   # question
#                   this_question = {
#                         "id": post.attrib["Id"],
#                         "title": post.attrib["Title"],
#                         "body": post.attrib["Body"],
#                         "accepted": post.attrib["AcceptedAnswerId"] if "AcceptedAnswerId" in post.attrib else -1  
#                   }
#                   questions[post.attrib["Id"]] = this_question
#       elif int(post.attrib["PostTypeId"]) == 2:
#             # answer
#             this_answer = {
#                   "id": post.attrib["Id"],
#                   "question_id": post.attrib["ParentId"],
#                   "body": post.attrib["Body"],
#             }
#             answers[post.attrib["Id"]] = this_answer

# # print(questions)
# # print(answers)

# print(f"There are {len(questions)} questions and {len(answers)} answers")


# I just made this so I can get the questions list for random sampling when making negative samples in build_evaluation
def get_question_dict():
      tree = ElementTree()
      tree.parse("data//Posts.xml")
      root = tree.getroot()
      posts = root.iter("row")

      questions = {}
      # first preprocess the data and split them into questions and answers
      for post in posts:
            if int(post.attrib["PostTypeId"]) == 1:
                  if "AnswerCount" in post.attrib and int(post.attrib["AnswerCount"]) > 0:
                        # question
                        this_question = {
                              "id": int(post.attrib["Id"]),
                              "title": post.attrib["Title"],
                              "body": post.attrib["Body"],
                              "accepted": post.attrib["AcceptedAnswerId"] if "AcceptedAnswerId" in post.attrib else -1  
                        }
                        questions[int(post.attrib["Id"])] = this_question

      # first question
      for id, value in questions.items():
            value["title"] = bs(value["title"], "lxml").text
            value["body"] = bs(value["body"], "lxml").text
            questions[id] = value
      # then answer
      # for id, value in answers.items():
      #       value["body"] = bs(value["body"], "lxml").text
      #       answers[id] = value

      return questions
