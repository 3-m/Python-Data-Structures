"""
DSAstack.py - an object oriented approach to implementing array and
              linked list based stacks
Classes:
DSAStack - An abstract base class outlining the methods of the Stack data
           structure
Stack - First in last out stack implementation using numpy object array
"""

from abc import ABC, abstractmethod
import numpy as np


class DSAStack(ABC):

    def __init__(self):
        self.count = 0
        super().__init__()

    @abstractmethod
    def getCount(self):
        pass

    @abstractmethod
    def isEmpty(self):
        pass

    @abstractmethod
    def isFull(self):
        pass

    @abstractmethod
    def push(self, value):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def top(self):
        pass

    @abstractmethod
    def display(self):
        pass


class Stack(DSAStack):

    def __init__(self, capacity=100):
        self.capacity = capacity
        self.stack = np.empty(self.capacity, dtype=object)
        super().__init__()

    def getCount(self):
        return self.count

    def isEmpty(self):
        empty = self.count == 0
        return empty

    def isFull(self):
        full = self.count == self.capacity
        return full

    def push(self, value):
        if self.isFull():
            raise StackOverflowError("Stack already full.")
        else:
            self.stack[self.count] = value
            self.count += 1

    def pop(self):
        if self.isEmpty():
            raise StackUnderflowError("No value since stack is empty")
        else:
            topVal = self.top()
            self.count -= 1

        return topVal

    def top(self):
        if self.isEmpty():
            raise StackUnderflowError("No value since stack is empty.")
        else:
            topVal = self.stack[self.count - 1]

        return topVal

    def __str__(self):
        outstring = ""
        for item in self.stack:
            outstring = outstring + ", " + str(item)
        return outstring[2:]

    def display(self):
        print(self)


class Error(Exception):
    pass


class StackOverflowError(Error):
    """Exception raised if stack is overfull.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class StackUnderflowError(Error):
    """Exception raised if stack is underfull.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
