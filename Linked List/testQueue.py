import unittest
import numpy as np
from linkedLists import *


class queueTest(unittest.TestCase):

    def test_queue_init(self):
        s = linkedQueue()
        self.assertIsInstance(s, linkedQueue)

    def test_queue_init_count(self):
        s = linkedQueue()
        self.assertEqual(s.count, 0)

    def test_is_empty(self):
        s = linkedQueue()
        self.assertTrue(s.isEmpty())

    def test_enqueue_one(self):
        s = linkedQueue(3)
        s.enqueue('abc')
        self.assertEqual(s.head.value, 'abc')

    def test_peek(self):
        s = linkedQueue(3)
        s.enqueue('abc')
        self.assertEqual(s.peek(), 'abc')

    def test_enqueue_multiple(self):
        s = linkedQueue(3)
        s.enqueue('abc')
        s.enqueue('dog')
        self.assertEqual(s.peek(), 'abc')

    def test_get_count(self):
        s = linkedQueue(3)
        s.enqueue('abc')
        s.enqueue('dog')
        self.assertEqual(s.getCount(), 2)

    def test_underflow(self):
        s = linkedQueue(1)
        with self.assertRaises(QueueUnderflowError):
            s.peek()

    def test_dequeue_empty_queue(self):
        s = linkedQueue(1)
        with self.assertRaises(QueueUnderflowError):
            s.dequeue()

if __name__ == '__main__':
    unittest.main()

