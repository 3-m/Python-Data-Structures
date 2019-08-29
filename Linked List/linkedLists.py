from abc import ABC, abstractmethod

class ListNode:

    def __init__(self, value=None):
        self.value = value
        self.nextNode = None
        self.prevNode = None


class DSALinkedList(ABC):

    @abstractmethod
    def __init__(self, head=None):
        self.head = head

    def insertFirst(self, newValue):
        ...

    def insertLast(self, newValue):
        ...

    def isEmpty(self):
        empty = self.head == None

        return empty

    def peekFirst(self):
        if self.isEmpty():
            raise Exception("No value returned since linked list is empty.")

        else:
            nodeValue = self.head.value

        return nodeValue

    def peekLast(self):
        ...

    def removeFirst(self):
        ...

    def removeLast(self):
        ...

class SingleLinkedList(DSALinkedList):

    def __init__(self, head=None):
        self.head = head

    def insertFirst(self, newValue):
        newNode = ListNode(newValue)

        if self.isEmpty():
            self.head = newNode
        else:
            newNode.nextNode = self.head
            self.head = newNode

    def insertLast(self, newValue):
        newNode = ListNode(newValue)

        if self.isEmpty():
            self.head = newNode

        else:
            currNode = self.head

            while currNode.nextNode != None:
                currNode = currNode.nextNode

            currNode.nextNode = newNode


    def isEmpty(self):
        return super().isEmpty()

    def peekFirst(self):
        return super().peekFirst()

    def peekLast(self):
        if self.isEmpty():
            raise Exception("No value returned since linked list is empty.")

        else:
            currNode = self.head

            while currNode.nextNode != None:
                currNode = currNode.nextNode

            nodeValue = currNode.value

        return nodeValue

    def removeFirst(self):
        if self.isEmpty():
            raise Exception("Nothing to remove since linked list is empty.")

        else:
            nodeValue = self.head.value
            self.head = self.head.nextNode

        return nodeValue

    def removeLast(self):
        if self.isEmpty():
            raise Exception("Nothing to remove since linked list is empty.")

        elif self.head.nextNode.nextNode == None:
            nodeValue = self.head.value
            self.head = None

        else:
            prevNode = None
            currNode = self.head

            while currNode.nextNode != None:
                prevNode = currNode
                currNode = currNode.nextNode

            prevNode.nextNode = None
            nodeValue = currNode.value

        return nodeValue


class DoublyLinkedList(DSALinkedList):

    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def insertFirst(self, newValue):
        newNode = ListNode(newValue)

        if self.isEmpty():
            self.head = newNode
            self.tail = newNode

        else:
            # link existing list to new head
            newNode.nextNode = self.head
            # set new head
            self.head = newNode
            # link previous head to new head
            self.head.nextNode.prevNode = self.head

    def insertLast(self, newValue):
        newNode = ListNode(newValue)

        if self.isEmpty():
            self.head = newNode
            self.tail = newNode

        else:
            # point old tail to new tail
            self.tail.nextNode = newNode
            # point new tail to the prev node
            newNode.prevNode = self.tail
            # set new tail
            self.tail = newNode

    def isEmpty(self):
        return super().isEmpty()

    def peekFirst(self):
        return super().peekFirst()

    def peekLast(self):
        if self.isEmpty():
            raise Exception("No value returned since linked list is empty.")

        else:
            nodeValue = self.tail.value

        return nodeValue

    def removeFirst(self):
        if self.isEmpty():
            raise Exception("Nothing to remove since linked list is empty.")

        elif self.head == self.tail:
            nodeValue = self.head.value
            self.head = None
            self.tail = None

        else:
            nodeValue = self.head.value
            self.head = self.head.nextNode
            self.head.prevNode = None

        return nodeValue

    def removeLast(self):
        if self.isEmpty():
            raise Exception("Nothing to remove since linked list is empty.")

        elif self.head == self.tail:
            nodeValue = self.head.value
            self.head = None
            self.tail = None

        else:
            nodeValue = self.tail.value
            self.tail = self.tail.prevNode
            self.tail.nextNode = None

        return nodeValue

    def __iter__(self):
        self.nodeValue = self.head
        return self

    def __next__(self):
        if self.nodeValue != None:
            nodeValue = self.nodeValue.value
            self.nodeValue = self.nodeValue.nextNode
        else:
            raise StopIteration
        return nodeValue

class linkedQueue(DSALinkedList):

    def __init__(self, head=None, tail=None):
        self.head = None
        self.tail = None
        self.count = 0

    def getCount(self):
        return self.count

    def isEmpty(self):
        empty = self.count == 0
        return empty

    def enqueue(self, inValue):
        newNode = ListNode(inValue)

        if self.isEmpty():
            self.head = newNode
            self.tail = newNode

        else:
            # point old tail to new tail
            self.tail.nextNode = newNode
            # point new tail to the prev node
            newNode.prevNode = self.tail
            # set new tail
            self.tail = newNode

        self.count += 1

    def dequeue(self):
        if self.isEmpty():
            raise QueueUnderflowError("The queue is already empty")

        if self.isEmpty():
            raise Exception("Nothing to remove since linked list is empty.")

        elif self.head == self.tail:
            nodeValue = self.head.value
            self.head = None
            self.tail = None

        else:
            nodeValue = self.head.value
            self.head = self.head.nextNode
            self.head.prevNode = None

        self.count += 1

        return nodeValue

    def peek(self):
        if self.isEmpty():
            raise QueueUnderflowError("No value since queue is empty.")
        topVal = self.head.value
        return topVal

class Error(Exception):
    pass

class QueueUnderflowError(Error):
    """Exception raised if queue is underfull.

    Attributes:
        message -- explanation of the error
    """

class linkedStack(DSALinkedList):

    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
        self.count = 0

    def getCount(self):
        return self.count

    def isEmpty(self):
        empty = self.count == 0
        return empty

    def push(self, value):

        newNode = ListNode(value)

        if self.isEmpty():
            self.head = newNode
            self.tail = newNode

        else:
            # point old tail to new tail
            self.tail.nextNode = newNode
            # point new tail to the prev node
            newNode.prevNode = self.tail
            # set new tail
            self.tail = newNode

        self.count += 1

    def pop(self):
        if self.isEmpty():
            raise StackUnderflowError("No value since stack is empty")

        elif self.head == self.tail:
            nodeValue = self.head.value
            self.head = None
            self.tail = None

        else:
            nodeValue = self.tail.value
            self.tail = self.tail.prevNode
            self.tail.nextNode = None

        self.count+=1

        return nodeValue

    def top(self):
        if self.isEmpty():
            raise StackUnderflowError("No value since stack is empty.")
        else:
            nodeValue = self.tail.value

        return nodeValue

    def display(self):
        print(self)


class StackUnderflowError(Error):
    """Exception raised if stack is underfull.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


