import numpy as np
import random
import gensim
from gensim.models import KeyedVectors
import gensim.downloader
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from collections import defaultdict
import pickle

lemmatizer = WordNetLemmatizer()

class GloveDataset():
    def __init__(self, filepath="../dataset/dataset.csv", lemmatize=True, save_model=False, save_name = "../dataset/glove.pkl"):
        self.df = pd.read_csv(filepath)
        self.lemmatize = lemmatize
        try:
            self.glove_embed = KeyedVectors.load('glove-wiki-gigaword-200.kv')
        except:
            self.glove_embed = gensim.downloader.load('glove-wiki-gigaword-200')
            self.glove_embed.save('glove-wiki-gigaword-200.kv')

        self.embed_size = self.glove_embed[0].shape[0]
        
        try:
            self.unk_embedding = np.load('unk_embedding.npy')
        except:
            self.unk_embedding = np.zeros((self.embed_size,))
            for index in range(len(self.glove_embed)):
                self.unk_embedding += self.glove_embed[index]
            self.unk_embedding /= len(self.glove_embed)
            np.save('unk_embedding.npy', self.unk_embedding)

        self.matrix = [] #  np.zeros((len(self.df), self.embed_size))
        self.data = []

        self.id_to_corpus = dict()
        self.corpus_to_id = dict()
        self.duplicate = defaultdict(lambda: []) # map doc_id to a duplicate doc_id (very similar questions)
        i = 1
        # only loading the titles for now 
        for index, row in self.df.iterrows():
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

            for doc_index, entry in [(cur_data["q1_id"], cur_data["q1_text"]), (cur_data["q2_id"], cur_data["q2_text"])]:
                if doc_index not in self.id_to_corpus:

                    self.id_to_corpus[doc_index] = len(self.matrix)
                    self.corpus_to_id[len(self.matrix)] = doc_index
                    e = self.embed_sentence(str(entry), lemmatize=self.lemmatize)
                    self.matrix.append(e)
                    if i == 1 or e.shape != (200,):
                        print(f"Adding {e.shape}")
                        i += 1
        print(f"From {len(self.matrix)}, {self.matrix[0].shape}")
        self.matrix = np.array(self.matrix)
        print(f"Resulting in {self.matrix.shape}")
        
        if save_model:
            try:
                print("Pickling Glove training data...")
                with open(save_name, "wb") as f:
                    pickle.dump(self.data, f)
                    print("Successfully wrote data")    
            except Exception as e:
                print("Some errors happened in pickling data")
                print(e)

    def embed_sentence(self, sentence, lemmatize):
        if lemmatize:

            # Convert a sentence into its embedded form for each word

            sentence = sentence.lower()
            tokens = word_tokenize(sentence)
            pos_tokens = nltk.pos_tag(tokens)

            # lemmatize
            
            def _lemmatize(token, pos):
                wordnet_pos = None
                if pos.startswith('J'):
                    wordnet_pos = wordnet.ADJ
                elif pos.startswith('V'):
                    wordnet_pos =  wordnet.VERB
                elif pos.startswith('N'):
                    wordnet_pos = wordnet.NOUN
                elif pos.startswith('R'):
                    wordnet_pos = wordnet.ADV
                else:
                    return lemmatizer.lemmatize(token)

                return lemmatizer.lemmatize(token, wordnet_pos)
            
            tokens = [_lemmatize(token, pos) for token, pos in pos_tokens]

            embedded = np.zeros((len(tokens), self.embed_size))
            for i, token in enumerate(tokens):
                if token in self.glove_embed:
                    embedded[i] = self.glove_embed[token]
                else:
                    embedded[i] = self.unk_embedding
            
            return embedded.mean(axis=0)
        else:
            sentence = sentence.lower()
            tokens = word_tokenize(sentence)
            embeddings = []
            # tokens = np.zeros((len(tokens), self.embed_size))
            
            for i, token in enumerate(tokens):
                if token in self.glove_embed:
                    embeddings.append(self.glove_embed[token])
            
            if len(embeddings) == 0:
                return self.unk_embedding
            return np.array(embeddings).mean(axis=0)