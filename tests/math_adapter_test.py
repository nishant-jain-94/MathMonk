import nltk
import unittest
from nltk.tree import Tree
from adapters import MathAdapter

class TestMathAdapter(unittest.TestCase):

	def test_ie_process(self):
		math_adapter = MathAdapter()
		tagged_tokens = math_adapter.ie_process("What is 2+3?")
		assert isinstance(tagged_tokens, list)
		assert len(tagged_tokens) > 0
		for tagged_tokens in tagged_tokens:
			assert isinstance(tagged_tokens, tuple)

	def test_chunk(self):
		math_adapter = MathAdapter()
		tagged_tokens = math_adapter.ie_process("What is 33+88?")
		expected_tree = Tree('S', [("What","WP"), ("is", "VBZ"), Tree("ME", [("33", "CD"), ("+", "OPERATOR"), ("88", "CD")])])
		actual_tree = math_adapter.chunk(tagged_tokens)
		assert isinstance(actual_tree, nltk.tree.Tree)
		assert expected_tree == actual_tree
		
		tagged_tokens = math_adapter.ie_process("What is 24 added by 67")
		expected_tree = Tree('S', [("What","WP"), ("is", "VBZ"), ("24", "CD"), ("added", "OPER_ADJ"), ("by", "IN"), ("67", "CD")])
		actual_tree = math_adapter.chunk(tagged_tokens)
		assert isinstance(actual_tree, nltk.tree.Tree)
		assert expected_tree == actual_tree

	def test_build_expression(self):
		math_adapter = MathAdapter()
		tagged_tokens = math_adapter.ie_process("What is 33+88")
		chunks = math_adapter.chunk(tagged_tokens)
		expected_expression = "33+88"
		actual_expression = math_adapter.build_expression(chunks)
		assert isinstance(actual_expression, str)
		assert expected_expression == actual_expression

		tagged_tokens = math_adapter.ie_process("What is 24+34+43 added by 67?")
		chunks = math_adapter.chunk(tagged_tokens)
		expected_expression = "(24+34+43)+(67)"
		actual_expression = math_adapter.build_expression(chunks)
		assert isinstance(actual_expression, str)
		assert expected_expression == actual_expression

	def test_compute(self):
		math_adapter = MathAdapter()
		actual_value = math_adapter.compute("What is 24+6+10 added by 60?")
		expected_value = "100.0"
		assert isinstance(actual_value, str)
		assert actual_value == expected_value

	def test_respond(self):
		math_adapter = MathAdapter()
		response = math_adapter.respond("What is 24+6+10 added by 60?")
		assert isinstance(response, str)	
		assert "100.0" in response

if __name__ == "__main__":
	unittest.main()