import unittest
from mathmonk import MathMonk

class TestMathMonk(unittest.TestCase):
	def test_get_response(self):
		mathmonk = MathMonk()
		response = mathmonk.get_response("What is two added by 24?")
		assert response != None
		assert isinstance(response, str)
		assert "26" in response

		response = mathmonk.get_response("Hi how are you?")
		assert response != None
		assert isinstance(response, str)