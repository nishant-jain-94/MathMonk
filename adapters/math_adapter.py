import nltk
import re
import numpy as np
from util import MathProcessor
from nltk import load_parser
from nltk import word_tokenize
from corpus import read_corpus
from comparisons import cosine_distance
from operator_tagger import OperatorTagger

class MathAdapter():

	def __init__(self):
		math_words = read_corpus('math_words', extension="json")
		self.operative_adjectives = math_words["operative_adjectives"]
		self.operators = math_words["operator_alias"]
		self.math_processor = MathProcessor()

	def ie_process(self, sentence):
		tokenized_words = re.findall(r"(\b\w*[\.]?\w+\b|[\(\)\+\*\-\/])", sentence)
		operator_tagger = OperatorTagger()
		tagged_words = operator_tagger.tag(tokenized_words)
		return tagged_words

	def chunk(self, tagged_sentence):
		grammar = r"""
		ME: {<CD><OPERATOR><CD>}
		"""
		cp = nltk.RegexpParser(grammar)
		tree = cp.parse(tagged_sentence)
		return tree

	def transform_chunk(self, expression, temp, chunk=None):
		if expression.endswith("("):
			temp.append(")")
		expression += ''.join(temp)
		if chunk:
			expression = "(" + expression + ")"
			expression += self.operative_adjectives[chunk[0]]
			expression += "("
		return expression
		
	def build_expression(self, chunked_sentence):
		expression = ""
		temp = []
		for chunk in chunked_sentence:
			if isinstance(chunk, nltk.tree.Tree) and chunk.label() == 'ME':
				temp.append(self.build_expression(chunk))
			elif chunk[1] == "CD":
				temp.append(chunk[0])
			elif chunk[1] == "OPERATOR":
				temp.append(self.operators[chunk[0]])
			elif chunk[1] == "OPER_ADJ":
				expression = self.transform_chunk(expression, temp, chunk)
				temp = []
		if temp: expression = self.transform_chunk(expression, temp)
		return expression


	def compute(self, sentence):
		tagged_sentence = self.ie_process(sentence)
		chunked_sentence = self.chunk(tagged_sentence)
		expression = self.build_expression(chunked_sentence)
		computed_value = None
		if len(set(['>', '<', '>=', '<=', '==', '!=']) & set(list(expression))) == 0:
			postfix_expression = self.math_processor.infix2postfix(expression)
			computed_value = str(self.math_processor.postfix_calculate(postfix_expression))
		else:
			computed_value = str(eval(expression))
		return computed_value
		

	def respond(self, sentence):
		rows = read_corpus('mathqa.corpus', extension="csv")
		cosine_scores = np.array([cosine_distance(sentence, data[0]) for data in rows])
		matched_response = rows[np.argmax(cosine_scores)]
		response = None
		try:
			computed_value = self.compute(sentence)
			response = matched_response[1].format(computed_value)
		except:
			response = matched_response[2]
		return response