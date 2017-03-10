import unittest
from comparisons import cosine_distance

class TestComparisons(unittest.TestCase):
	def test_cosine_distance(self):
		distance = cosine_distance("What is 2+4", "What is 2+4")
		assert isinstance(distance, float)
		assert int(distance) == 1