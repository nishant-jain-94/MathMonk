import unittest
from nltk import word_tokenize
from util import MathProcessor 

class TestMathProcessors(unittest.TestCase):

	def test_get_math_words(self):
		math_processor = MathProcessor()
		math_words = math_processor.get_math_words()
		assert math_words != None

	def test_text2int(self):
		math_processor = MathProcessor()
		text2int = math_processor.text2int(['seven', 'thousand', 'five', 'hundred', 'fifty', 'five'])
		assert text2int == "7555"

	def test_transform_text(self):
		math_processor = MathProcessor()
		transformed_text = math_processor.transform_text('what is seven thousand five hundred fifty five plus five')
		assert transformed_text == "what is 7555 plus 5"
		transformed_text = math_processor.transform_text('What is 7555 plus 5?')
		assert transformed_text == "What is 7555 plus 5 ?"

	def test_infix2postfix(self):
		math_processor = MathProcessor()
		infix_notation = list(math_processor.infix2postfix('2+3+10*5'))
		assert infix_notation == ['2', '3', '+', '10', '5', '*', '+']

	def test_postfix_calculate(self):
		math_processor = MathProcessor()
		calculated_value = math_processor.postfix_calculate(list(math_processor.infix2postfix('2+3+10*5')))
		assert calculated_value == 55

if __name__ == '__main__':
	unittest.main()