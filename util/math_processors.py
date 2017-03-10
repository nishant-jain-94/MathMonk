import json
import os
from corpus import read_corpus
from nltk import word_tokenize

class MathProcessor():

	def __init__(self):
		self.math_words = self.get_math_words()

	def transform_text(self, sentence):
		transformed_text = []
		temp = []
		tokenized_words = word_tokenize(sentence)
		for word in tokenized_words:
			if word in self.math_words['numbers'] or word in self.math_words['scales']:
				temp.append(word)
			else:
				if temp:
					transformed_text.append(self.text2int(temp))
					temp = []
				transformed_text.append(word)
		if temp: transformed_text.append(self.text2int(temp))
		return ' '.join(transformed_text)

	def text2int(self, numwords):
		current = result = 0
		for word in numwords:
			if word in self.math_words['numbers']:
				scale, increment = 1, self.math_words['numbers'][word]
			else:
				scale, increment = self.math_words['scales'][word], 0
			current = current * scale + increment
			if scale > 100:
				result += current
				current = 0
		return str(result + current)

	def get_math_words(self):
		data = read_corpus('math_words', extension="json")
		return data

	def infix2postfix(self, expression):
	    """Converts an Infix expression to a Postfix expression
	    expression: input an infix expression
	    Returns: an postfix expression
	    """
	    stack = []
	    stack.append('e');
	    number_str=''
	    operators = list(self.math_words['operators'].values())

	    for token in expression:
	        if not token.isdigit() and number_str:
	            yield number_str
	            number_str = ""
	        
	        if token in operators:
	            while True:
	                if self.math_words["operator_precedence"][token] > self.math_words["operator_precedence"][stack[-1]]:
	                    stack.append(token)
	                    break
	                else:
	                    yield stack.pop()
	                    
	        elif token.isdigit():
	            number_str += token
	                    
	        elif token == "(":
	            stack.append(token)
	            
	        elif token == ")":
	            while True:
	                ch = stack.pop()
	                if ch == "(":
	                    break
	                else:
	                    yield ch
	    if number_str:
	        yield number_str
	        
	    for s in reversed(stack[1:]):
	        yield s
	
	def postfix_calculate(self, iterator):
	    """Performs calculation over postfix expression.
	    iterator: inputs an postfix iterator
	    Returns: a calculated value of the postfix expression
	    """
	    func_map = {
	    	"+": lambda x, y: x + y,
		    "-": lambda x, y: x - y,
	    	"*": lambda x, y: x * y,
	    	"/": lambda x, y: x / y,
	    	"^": lambda x, y: x ^ y
		}
	    stack = []
	    for ch in iterator:
	        try:
	            stack.append(float(ch))
	        except ValueError:
	            func = func_map[ch]
	            y = stack.pop()
	            x = stack.pop()
	            stack.append(func(x, y))
	    return stack[0]

