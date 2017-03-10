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
	"""The MathAdapter parses the input to determine the type of operation. 
	And then follow series of steps to compute the result of an Operation.
	MathAdapter currently performs only basic arithmetic operations (+ , -, *, /)

	Performs the following Steps:
	1. Information Extraction
	2. Chunking
	3. Building Expression
	4. Computing the result of the expression
	5. Finding the best suited reply for the query
	"""

	def __init__(self):
		math_words = read_corpus('math_words', extension="json")
		self.operative_adjectives = math_words["operative_adjectives"]
		self.operators = math_words["operator_alias"]
		self.math_processor = MathProcessor()

	def ie_process(self, sentence):
		"""Tokenizes and Tags words in a sentence.
		
		sentence - inputs a sentence
		Returns a list of tuple containing the token and the tag
		"""
		tokenized_words = re.findall(r"(\b\w*[\.]?\w+\b|[\(\)\+\*\-\/])", sentence)
		operator_tagger = OperatorTagger()
		tagged_words = operator_tagger.tag(tokenized_words)
		return tagged_words

	def chunk(self, tagged_sentence):
		"""Chunks a tagged sentence into a Mathematical Expression. 
		A Mathematical Expression is a sequence of a Number followed by Operator followed by a Number.

		tagged_sentence - inputs a tagged_sentence
		Returns a Tree 
		"""
		grammar = r"""
		ME: {<CD><OPERATOR><CD>}
		"""
		cp = nltk.RegexpParser(grammar)
		tree = cp.parse(tagged_sentence)
		return tree

	def glue_chunks(self, expression, other_expression, chunk=None):
		"""Glues one expression with another. 
		Takes care of precedence by adjusting parantheses		
		
		expression - (str) mathematical expression
		other_expression - (str) mathematical expression
		chunk - (tuple) containing the operator
		Returns - (str) an transformed expression 
		"""
		if expression.endswith("("):
			other_expression.append(")")
		expression += ''.join(other_expression)
		if chunk:
			expression = "(" + expression + ")"
			expression += self.operative_adjectives[chunk[0]]
			expression += "("
		return expression
		
	def build_expression(self, chunked_sentence):
		"""Builds a Mathematical Expression from the chunks.
		
		chunked_sentence - Inputs a chunked sentence
		Returns a Mathematical Expression in Infix Notation 
		"""
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
				expression = self.glue_chunks(expression, temp, chunk)
				temp = []
		if temp: expression = self.glue_chunks(expression, temp)
		return expression


	def compute(self, sentence):
		"""Performs Mathematical Operation on the Natural Language Input and returns a computed Value.
		
		sentence - (str) Inputs a sentence in Natural Language
		Returns a computed value of the mathematical operation
		"""
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
		"""Performs Mathematical Operation on the Natural Language Input and 
		returns a response in Natural Language containing the computed value.
		
		sentence - (str) Inputs a sentence in Natural Language
		Returns - (str) best matched response 
		"""
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