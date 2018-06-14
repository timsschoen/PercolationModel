import unittest
from priority_queue import PriorityQueue

class TestPriorityQueue(unittest.TestCase):
	
	def test_contains(self):
		Q = PriorityQueue()
		Q.add_update(1, 0)

		self.assertTrue(1 in Q)
		self.assertFalse(2 in Q)

	def test_pop(self):
		Q = PriorityQueue()
		Q.add_update(1, 1)
		Q.add_update(2, 0)

		self.assertEqual(Q.pop(), 2)

		Q.add_update(3, 0.5)

		self.assertEqual(Q.pop(), 3)
		self.assertEqual(Q.pop(), 1)

	def test_update(self):
		Q = PriorityQueue()
		Q.add_update(1, 2)
		Q.add_update(2, 1)		
		Q.add_update(1, 0)

		self.assertEqual(Q.pop(), 1)

if __name__ == "__main__":
	unittest.main()