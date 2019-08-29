class TreeNode:

    def __init__(self, inKey, inValue):
        if inKey is None:
            raise EmptyKeyTreeError("Key cannot be empty")
        self._key = inKey
        self._value = inValue
        self._leftChild = None
        self._rightChild = None

class BinaryTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def find(self, key):
        """Find wrapper method for Binary Search Tree

        Attributes:
            key - key value to search for
        """

        return self._findRecursive(key, self.root)

    def _findRecursive(self, key, currNode):
        value = None

        if currNode == None:
            raise Exception("Base case - not found")

        elif currNode._key == key:
            value = currNode._value

        elif currNode._key > key:
            value = self._findRecursive(key, currNode._leftChild)

        else:
            value = self._findRecursive(key, currNode._rightChild)

        return value

    def insert(self, key, value):
        """Insert recursive method for Binary Search Tree

        Attributes:
            key - key value to input
            value - value associated with the key
        """
        if self.root == None:
            self.root = TreeNode(key, value)

        else:
            self._insertRecursive(key, value, self.root)

    def _insertRecursive(self, key, value, currNode):

        updateNode = currNode

        if currNode == None:
            newNode = TreeNode(key, value)
            updateNode = newNode

        elif key == currNode._key:
            raise Exception(f"Key already exists in tree: {currNode._key}")

        elif key < currNode._key:
            currNode._leftChild = self._insertRecursive(key, value, currNode._leftChild)

        else:
            currNode._rightChild = self._insertRecursive(key, value, currNode._rightChild)

        return updateNode

    def delete(self, key):
        return self._delete(key, self.root)

    def _delete(self, key, currNode):

        updateNode = None

        if key == currNode._key:

            if currNode._rightChild != None and currNode._leftChild == None:
                updateNode = currNode._rightChild

            elif currNode._leftChild != None and currNode._rightChild == None):





        elif key < currNode:
            currNode._leftChild = self._delete(key, currNode._leftChild)

        else:
            currNode._rightChild = self._delete(key, currNode._rightChild)



    def height(self):
        ...


class Error(Exception):
    pass

class EmptyKeyTreeError(Error):
    """Exception called when tree node is initialised with no value."""

t = BinaryTree()
t.insert(10, 10)
t.insert(3, 3)
t.insert(1, 1)
