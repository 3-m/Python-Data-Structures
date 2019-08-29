"""
Classes:
Queue - First in first out Queue implementation using numpy object array with
        shuffling when an object is removed
Circular Queue - No shuffling of the object array when object is removed
"""

import numpy as np


class Queue:

    def __init__(self, capacity=100):
        self.capacity = capacity
        self.queue = np.empty(self.capacity, dtype=object)
        self.count = 0

    def getCount(self):
        return self.count

    def isEmpty(self):
        empty = self.count == 0
        return empty

    def isFull(self):
        full = self.count == self.capacity
        return full

    def enqueue(self, value):
        if self.isFull():
            raise QueueOverflowError("The queue is already full.")

        self.queue[self.count] = value
        self.count += 1

    def dequeue(self):
        if self.isEmpty():
            raise QueueUnderflowError("The queue is already empty")

        frontVal = self.queue[0]

        for i in range(1, self.count + 1):
            self.queue[i - 1] = self.queue[i]

        self.count -= 1

        return frontVal

    def peek(self):
        if self.isEmpty():
            raise QueueUnderflowError("No value since queue is empty.")
        topVal = self.queue[0]
        return topVal

    def __str__(self):
        contents = ''

        for item in range(self.count):
            contents += f"{self.queue[item]}\n"

        return contents


class CircularQueue(Queue):

    def __init__(self, capacity):
        super().__init__(capacity)
        self.tail = 0
        self.head = 0

    def enqueue(self, value):
        if self.isFull():
            raise QueueOverflowError("The queue is already full.")

        self.queue[self.tail % self.capacity] = value
        self.count += 1
        self.tail += 1

    def dequeue(self):
        if self.isEmpty():
            raise QueueUnderflowError("The queue is already empty")

        frontVal = self.queue[self.head]
        self.head += 1
        self.count -= 1

        return frontVal

    def peek(self):
        if self.isEmpty():
            raise QueueUnderflowError("No value since queue is empty.")
        topVal = self.queue[self.head]
        return topVal


class Error(Exception):
    pass


class QueueOverflowError(Error):
    """Exception raised if queue is overfull.

    Attributes:
        message -- explanation of the error
    """


class QueueUnderflowError(Error):
    """Exception raised if queue is underfull.

    Attributes:
        message -- explanation of the error
    """
