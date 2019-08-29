import unittest
import numpy as np
from linkedLists import *


class StackTest(unittest.TestCase):

    def test_stack_init(self):
        s = linkedStack()
        self.assertIsInstance(s, linkedStack)

    def test_stack_init_count(self):
        s = linkedStack()
        self.assertEqual(s.count, 0)

    def test_is_empty(self):
        s = linkedStack(3)
        self.assertTrue(s.isEmpty())

    def test_push_one(self):
        s = linkedStack(3)
        s.push('abc')
        self.assertEqual(s.head.value, 'abc')

    def test_top(self):
        s = linkedStack(3)
        s.push('abc')
        self.assertEqual(s.top(), 'abc')

    def test_push_multiple(self):
        s = linkedStack(3)
        s.push('abc')
        s.push('dog')
        self.assertEqual(s.top(), 'dog')

    def test_get_count(self):
        s = linkedStack(3)
        s.push('abc')
        s.push('dog')
        self.assertEqual(s.getCount(), 2)

    def test_underflow(self):
        s = linkedStack(1)
        with self.assertRaises(StackUnderflowError):
            s.top()

    def test_pop_empty_stack(self):
        s = linkedStack(1)
        with self.assertRaises(StackUnderflowError):
            s.pop()


if __name__ == '__main__':
    unittest.main()

