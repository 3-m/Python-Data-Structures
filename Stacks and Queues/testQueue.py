import unittest
import numpy as np
from DSAqueue import *


class queueTest(unittest.TestCase):

    def test_queue_init(self):
        s = Queue()
        self.assertIsInstance(s.queue, np.ndarray)

    def test_queue_init_count(self):
        s = Queue()
        self.assertEqual(s.count, 0)

    def test_queue_default_capacity(self):
        s = Queue()
        self.assertEqual(s.capacity, 100)

    def test_queue_set_capacity(self):
        s = Queue(3)
        self.assertEqual(s.capacity, 3)

    def test_is_empty(self):
        s = Queue(3)
        self.assertTrue(s.isEmpty())

    def test_enqueue_one(self):
        s = Queue(3)
        s.enqueue('abc')
        self.assertEqual(s.queue[0], 'abc')

    def test_peek(self):
        s = Queue(3)
        s.enqueue('abc')
        self.assertEqual(s.peek(), 'abc')

    def test_enqueue_multiple(self):
        s = Queue(3)
        s.enqueue('abc')
        s.enqueue('dog')
        self.assertEqual(s.peek(), 'abc')

    def test_get_count(self):
        s = Queue(3)
        s.enqueue('abc')
        s.enqueue('dog')
        self.assertEqual(s.getCount(), 2)

    def test_is_full(self):
        s = Queue(1)
        s.enqueue('abc')
        self.assertTrue(s.isFull())

    def test_overflow(self):
        s = Queue(1)
        with self.assertRaises(QueueOverflowError):
            s.enqueue('abc')
            s.enqueue('abc')

    def test_underflow(self):
        s = Queue(1)
        with self.assertRaises(QueueUnderflowError):
            s.peek()

    def test_dequeue_empty_queue(self):
        s = Queue(1)
        with self.assertRaises(QueueUnderflowError):
            s.dequeue()

    def test_circular_queue(self):
        s = CircularQueue(3)
        s.enqueue(123)
        s.enqueue('abc')
        s.enqueue('dog')
        self.assertEqual(s.head, 0)
        s.dequeue()
        self.assertEqual(s.head, 1)
        s.enqueue('blah')
        self.assertEqual(s.queue[0], 'blah')


if __name__ == '__main__':
    unittest.main()

