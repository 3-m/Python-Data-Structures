import unittest
import numpy as np
from DSAstack import *


class StackTest(unittest.TestCase):

    def test_stack_init(self):
        s = Stack()
        self.assertIsInstance(s.stack, np.ndarray)
        print("Test: stack initialised")

    def test_stack_init_count(self):
        s = Stack()
        self.assertEqual(s.count, 0)
        print("Test: stack initialised empty")

    def test_stack_default_capacity(self):
        s = Stack()
        self.assertEqual(s.capacity, 100)
        print("Test: stack default capacity is 100")

    def test_stack_set_capacity(self):
        s = Stack(3)
        self.assertEqual(s.capacity, 3)
        print("Test: stack capacity initialised to 3")

    def test_is_empty(self):
        s = Stack(3)
        self.assertTrue(s.isEmpty())
        print("Test: isEmpty method returns True on empty stack")

    def test_push_one(self):
        s = Stack(3)
        s.push('abc')
        self.assertEqual(s.stack[0], 'abc')
        print("Test: push one object on stack and then check first stack element")

    def test_top(self):
        s = Stack(3)
        s.push('abc')
        self.assertEqual(s.top(), 'abc')
        print("Test: push one object on stack and check top() method")

    def test_push_multiple(self):
        s = Stack(3)
        s.push('abc')
        s.push('dog')
        self.assertEqual(s.top(), 'dog')
        print("Test: push two objects on stack and check that second object is on top")

    def test_get_count(self):
        s = Stack(3)
        s.push('abc')
        s.push('dog')
        self.assertEqual(s.getCount(), 2)
        print("Test: push two objects to stack and check count is 2")

    def test_is_full(self):
        s = Stack(1)
        s.push('abc')
        self.assertTrue(s.isFull())
        print("Test: fill stack and check isFull() method returns True")

    def test_overflow(self):
        s = Stack(1)
        with self.assertRaises(StackOverflowError):
            s.push('abc')
            s.push('abc')
        print("Test: stack overflow exception raised when pushing object onto full stack")

    def test_underflow(self):
        s = Stack(1)
        with self.assertRaises(StackUnderflowError):
            s.top()
        print("Test: attempting to perform top() method on empty stack raises stack underflow exception")

    def test_pop_empty_stack(self):
        s = Stack(1)
        with self.assertRaises(StackUnderflowError):
            s.pop()
        print("Test: attempt to pop empty stack raises stack underflow exception")


if __name__ == '__main__':
    unittest.main()

