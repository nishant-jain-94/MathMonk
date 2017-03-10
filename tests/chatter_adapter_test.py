import nltk
import unittest
from adapters import ChatterAdapter

class TestChatterAdapter(unittest.TestCase):
	
	def test_respond(self):
		chatter_adapter = ChatterAdapter()
		response = chatter_adapter.respond("Hi How are you")
		assert response != None
		assert isinstance(response, str)

if __name__ == "__main__":
	unittest.main()