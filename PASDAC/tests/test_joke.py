from unittest import TestCase 

import PASDAC

class TestJoke(TestCase):
	def test_is_string(self):
		s = PASDAC.smooth_joke()
		self.assertTrue(isinstance(s, str))

