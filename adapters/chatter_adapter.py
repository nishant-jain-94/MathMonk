import nltk
import numpy as np
from corpus import read_corpus
from comparisons import cosine_distance

class ChatterAdapter():
	
	def respond(self, sentence):
		rows = read_corpus('conversations.corpus', extension="csv")
		cosine_scores = np.array([cosine_distance(sentence, data[0]) for data in rows])
		matched_response = rows[np.argmax(cosine_scores)]
		return matched_response[1]
	    