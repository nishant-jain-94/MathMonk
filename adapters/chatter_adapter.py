import nltk
import numpy as np
from corpus import read_corpus
from comparisons import cosine_distance

class ChatterAdapter():
	
	def respond(self, sentence):
		"""Finds the best suitable response for the sentence given and responds it back
		
		sentence - (str) Inputs a sentence in Natural Language
		Returns - (str) a best matched response
		"""
		rows = read_corpus('conversations.corpus', extension="csv")
		cosine_scores = np.array([cosine_distance(sentence, data[0]) for data in rows])
		matched_response = rows[np.argmax(cosine_scores)]
		return matched_response[1]
	    