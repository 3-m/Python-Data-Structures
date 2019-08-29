"""
FILE: dsaTrees.py
AUTHOR: Matteo Miceli
USERNAME: 18910854
UNIT: COMP1002 Data Structures and Algorithms
PURPOSE: Implementation of Binary Search Tree, B-tree and an unordered binary
         tree
REFERENCE: Binary tree based on own code written in Practical 1,
           COMP1002 Data Structures and Algorithms (2019). Others specified in
           function docstring.
COMMENTS: b-tree delete function seems to work - yet to find a test case where it fails
REQUIRES: numpy - object arrays, sys - increase recursion limit to prevent stack
          overflow in degenerate trees, dsaLinkedList - used to store the tree
          in order prior to writing to csv, timeit - used to calculate the
          run time of insert, delete, find and sorting/generating the linkedList
          for export.
Last Mod: 04/06/2019
"""
from abc import ABC
import numpy as np
import sys
from .dsaLinkedList import dsaLL
from timeit import default_timer as timer

class dsaTree(ABC):
    def find(self):
        ...

    def insert(self):
        ...

    def delete(self):
        ...

    def height(self):
        ...

    def balance(self):
        ...

    def storeTree(self):
        ...

class _BinaryTreeNode:

    def __init__(self, inKey, inValue):
        if inKey is None:
            raise EmptyKeyTreeError("Key cannot be empty")
        self._key = inKey
        self._value = inValue
        self._leftChild = None
        self._rightChild = None


class BinaryTree(dsaTree):

    def __init__(self):
        self.root = None
        self.size = 0
        self.insTime = 0.
        self.delTime = 0.
        self.findTime = 0.
        self.sortTime = 0.

    #https://stackoverflow.com/questions/12444004/how-long-does-my-python-application-take-to-run
    def find(self, key):
        """Find wrapper method for Binary Search Tree

        Attributes:
            key - key value to search for
        """
        startT = timer()
        result = self._findRecursive(key, self.root)
        elapsedT = timer() - startT
        self.findTime += elapsedT

        return result

    def _findRecursive(self, key, currNode):
        value = None

        if currNode is None:
            raise KeyNotFoundTreeError("Base case - not found")

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
        startT = timer()
        self.size += 1

        if self.root is None:
            self.root = _BinaryTreeNode(key, value)

        else:
            self._insertRecursive(key, value, self.root)

        elapsedT = timer() - startT
        self.insTime += elapsedT

    def _insertRecursive(self, key, value, currNode):

        updateNode = currNode

        if currNode is None:
            newNode = _BinaryTreeNode(key, value)
            updateNode = newNode

        elif key == currNode._key:
            raise TreeNodeError( f"Key {currNode._key} already exists "
                                  "in tree." )

        elif key < currNode._key:
            currNode._leftChild = self._insertRecursive(key,
                                                        value,
                                                        currNode._leftChild)

        else:
            currNode._rightChild = self._insertRecursive(key,
                                                         value,
                                                         currNode._rightChild)

        return updateNode

    def delete(self, key):
        startT = timer()
        self.size -= 1
        result = self._delete(key, self.root)
        elapsedT = timer() - startT
        self.delTime += elapsedT
        return result

    def _delete(self, key, currNode):

        updateNode = currNode

        if currNode is None:
            raise KeyNotFoundTreeError( f"No node found containing key: {key}" )
        elif key == currNode._key:
            updateNode = self._deleteNode(key, currNode)
        elif key < currNode._key:
            currNode._leftChild = self._delete(key, currNode._leftChild)
        else:
            currNode._rightChild = self._delete(key, currNode._rightChild)

        return updateNode

    def _deleteNode( self, key, delNode ):
        updateNode = None

        if ( ( delNode._leftChild is None ) and
             ( delNode._rightChild is None ) ):
             updateNode = None

        elif ( ( delNode._leftChild is not None ) and
               ( delNode._rightChild is None ) ):
             updateNode = delNode._leftChild

        elif ( ( delNode._leftChild is None ) and
             ( delNode._rightChild is not None ) ):
             updateNode = delNode._rightChild

        else:
            updateNode = self._promoteSuccessor( delNode._rightChild )

            if updateNode != delNode._rightChild:
                updateNode._rightChild = delNode._rightChild

            updateNode._leftChild = delNode._leftChild

        return updateNode

    def _promoteSuccessor(self, currNode):
        successor = currNode

        if currNode._leftChild is not None:
            successor = self._promoteSuccessor( currNode._leftChild )

            if successor == currNode._leftChild:
                currNode._leftChild = successor._rightChild

        return successor


    def height( self ):
        height = self._height( self.root )
        return height

    def _height( self, currNode ):
        leftHeight = 0
        rightHeight = 0
        htSoFar = 0

        if currNode is None:
            htSoFar = -1

        else:
            leftHeight = self._height( currNode._leftChild )
            rightHeight = self._height( currNode._rightChild )

            if leftHeight > rightHeight:
                htSoFar = leftHeight + 1
            else:
                htSoFar = rightHeight + 1

        return htSoFar

    #https://stackoverflow.com/questions/2598437/how-to-implement-a-binary-tree
    def storeTree(self):
        startT = timer()
        linkedList = dsaLL()

        if self.root._leftChild is not None:
            self._storeTree(self.root._leftChild, linkedList)
        if self.root is not None:
            linkedList.insertLast(self.root._value)
        if self.root._rightChild is not None:
            self._storeTree(self.root._rightChild, linkedList)
        elapsedT = timer() - startT
        self.sortTime = elapsedT
        return  linkedList

    def _storeTree(self, currNode,  linkedList):

        if currNode._leftChild is None and currNode._rightChild is None:
            linkedList.insertLast(currNode._value)

        elif currNode._leftChild is None:
            linkedList.insertLast(currNode._value)

        elif currNode._leftChild is not None:
            self._storeTree(currNode._leftChild, linkedList)
            #linkedList.insertLast(currNode._value)

        if currNode._rightChild is None and currNode._leftChild is not None:
            linkedList.insertLast(currNode._value)

        elif currNode._rightChild is not None:
            self._storeTree(currNode._rightChild, linkedList)


    def __iter__( self ):
        linkedList = self.storeTree()
        for share in linkedList:
            yield share


    def balance(self):
        numNodesComplete = 2**self.height() - 1

        balance = round((self.size/numNodesComplete) * 100, 2)

        return balance

class BTreeItem:
    def __init__( self, key=None, value=None ):
        self.key = key
        self.value = value

    def _displayItem( self ):
        print(f"/{self.key}", end= "")

class BTreeNode:

    def __init__( self, order):
        self.order = order
        self.numItems = 0
        self.pNode = None
        self.cArray = np.empty(self.order, dtype=object)
        self.itemArray = np.empty(self.order - 1, dtype=object)
        self.minKey = self.order // 2

    def connectChild( self, cNum, cNode, shift = 0):
        if shift == 1:
            for i in range(self.order - 1, 0, -1):
                self.cArray[i] = self.cArray[i - 1]

        self.cArray[cNum] = cNode

        if cNode is not None:
            cNode.pNode = self



    def disconnectChild( self, cNum, shift = 0):
        tempNode = self.cArray[cNum]
        self.cArray[cNum] = None

        if shift == 1:
            for i in range(cNum, self.numItems + 1):
                self.cArray[i] = self.cArray[i + 1]
            for j in range(self.numItems + 1, self.order):
                self.cArray[j] = None

        return tempNode

    def _countChild( self ):
        count = 0
        array = self.cArray

        if array[0] is not None:
            for i in range( len( array ) ):
                if array[i] is not None:
                    count += 1

        return count

    def isLeaf( self ):
        status = ( self.cArray[0] is None )
        return status

    def isFull( self ):
        status = ( self.numItems == (self.order - 1) )
        return status

    def findItem( self, searchKey ):
        isFound = False
        i = 0
        index = -1

        while ( isFound is False ) and ( i < self.numItems ):
            if self.itemArray[i].key == searchKey:
                index = i
                isFound = True
            else:
                index = -1
                i += 1

        return index

    def insertItem( self, newItem ):

        if self.isFull() is True:
            raise TreeNodeError("Node already full. Cannot add item.")

        if self.itemArray[0] is not None:
            isInserted = False
            i = self.order - 2

            while ( isInserted is False ) and ( i >= 0 ):
                if self.itemArray[i] is not None:
                    if newItem.key < self.itemArray[i].key:
                        self.itemArray[i + 1] = self.itemArray[i]
                        self.itemArray[i] = None
                    else:
                        self.itemArray[i + 1] = newItem
                        itemIndex = i + 1
                        isInserted = True

                i -= 1

        if self.itemArray[0] is None:
            self.itemArray[0] = newItem
            itemIndex = 0

        self.numItems += 1

        return itemIndex

    def removeItem(self, itemNum):

        if itemNum <= self.numItems:
            temp = self.itemArray[itemNum]

            for i in range(itemNum, self.order - 2):
                self.itemArray[i] = self.itemArray[i + 1]

            self.itemArray[self.order - 2] = None

            self.numItems -= 1

        else:
            raise TreeNodeError( "Can not remove node element that is greater"
                                 f" than node order. Order: {self.order}" )
        return temp

    def _displayNode(self):
        for i in range(0, self.numItems):
            self.itemArray[i]._displayItem()
        print('/')


    def __iter__(self):
        for i in range(self.numItems):
            yield self.itemArray[i].value


""" Algorithm based on Robert Lafore, "Data Structures and Algorithms in
    Java (Second Edition)" (2002), page 479. """
class BTree(dsaTree):

    def __init__(self, order = 4):
        self.order = order
        self.root = BTreeNode(order)
        self.size = 0
        self.insTime = 0
        self.delTime = 0
        self.findTime = 0
        self.sortTime = 0
        self.ht = 0

    def find( self, key ):
        startT = timer()
        currNode = self.root
        found = False
        item = None

        while found is False:
            childNum = currNode.findItem(key)

            if childNum != -1:
                found = True
                item = currNode.itemArray[childNum]

            elif currNode.isLeaf() is True:
                childNum = -1
                found = True

            else:
                currNode = self.getNextChild(key, currNode)

        if childNum == -1:
            raise KeyNotFoundTreeError( "Key does not exist in tree." )

        elapsedT = timer() - startT
        self.findTime += elapsedT

        return childNum, item


    def insert( self, key, value ):
        startT = timer()
        currNode = self.root
        tempItem = BTreeItem(key, value)
        isInserted = False
        keyExists = False

        try:
            keyExists = self.find(key)[0] != -1
        except KeyNotFoundTreeError:
            if ( self.size > 0 ) and ( keyExists ):
                raise TreeNodeError( f"Key {key} already exists in tree. "
                                      "Cannot add an existing key." )

            while not isInserted:
                if currNode.isFull() is True:
                    self.split(currNode)
                    currNode = currNode.pNode
                    currNode = self.getNextChild(key, currNode)

                elif currNode.isLeaf() is True:
                    currNode.insertItem(tempItem)
                    isInserted = True

                else:
                    currNode = self.getNextChild(key, currNode)

        self.size += 1
        elapsedT = timer() - startT
        self.insTime += elapsedT


    def split( self, node ):

        if node.isFull() is False:
            raise TreeNodeError("Attempting to split node that is not full.")

        splitPoint = ((self.order)//2) - 1
        newNodeShares = dsaLL()
        newNodeChildren = dsaLL()

        for i in range(splitPoint + 1, self.order - 1):
            item = node.removeItem(node.numItems - 1)
            newNodeShares.insertFirst(item)

        newParent = node.removeItem(splitPoint)

        for j in range(splitPoint + 1, self.order):
            child = node.disconnectChild(j)
            newNodeChildren.insertLast(child)

        rightNode = BTreeNode(self.order)

        if node == self.root:
            self.ht += 1
            self.root = BTreeNode(self.order)
            pNode = self.root
            self.root.connectChild(0, node)

        else:
            pNode = node.pNode

        itemIndex = pNode.insertItem(newParent)

        for i in range(pNode.numItems - 1, itemIndex, -1):
            temp = pNode.disconnectChild(i)
            pNode.connectChild(i + 1, temp)

        pNode.connectChild(itemIndex + 1, rightNode)

        for item in newNodeShares:
            rightNode.insertItem(item)

        idx = 0
        for child in newNodeChildren:
            rightNode.connectChild(idx, child)
            idx += 1

    def getNextChild( self, key, node):
        nextChild = -1
        isLess = False

        i = 0
        while ( isLess is False ) and ( i < node.numItems ):
            comparedKey = node.itemArray[i].key
            if key < comparedKey:
                nextChild = node.cArray[i]
                isLess = True
            i += 1

        if nextChild == -1:
            nextChild = node.cArray[node.numItems]

        return nextChild

    def delete( self, key ):
        startT = timer()
        found = self.find(key)[1]
        self._delete(key, self.root, self.root)

        #node.itemArray[cNum].value = None
        self.size -= 1
        elapsedT = timer() - startT
        self.delTime += elapsedT

        return found.value

    def _delete( self, key, node, root=0):
        itemLoc = node.findItem(key)
        if node.isLeaf() is True and itemLoc != - 1 and node.numItems >= node.minKey:
            node.removeItem(itemLoc)

        elif node.isLeaf() is False and itemLoc != -1:
            leftChild = node.cArray[itemLoc]
            rightChild = node.cArray[itemLoc + 1]

            if leftChild.numItems >= node.minKey:
                #get pred key
                predKey = self.getPredKey(key, node, itemLoc)
                # remove element of interest
                node.removeItem(itemLoc)
                # insert predecessor
                node.insertItem(predKey)
                # recursively delete predKey
                self._delete(predKey.key, leftChild)
                # check if root was removed
                if node == self.root and node.numItems == 0:
                    self.root = leftChild

            elif rightChild.numItems >= node.minKey:
                # get successor key
                succKey = self.getSuccKey(key, node, itemLoc)
                # remove element of interest
                node.removeItem(itemLoc)
                # insert successor
                node.insertItem(succKey)
                # rec del succKey
                self._delete(succKey.key, rightChild, node)
                # check if root was removed
                if node == self.root and node.numItems == 0:
                    self.root = rightChild

            elif rightChild.numItems < rightChild.minKey and leftChild.numItems < leftChild.minKey:
                # remove element from internal node
                item = node.removeItem(itemLoc)
                # insert into left child
                leftChild.insertItem(item)
                # merge right child into left child
                self.mergeNodes(rightChild, leftChild, node)
                # rec del element from left child
                self._delete(key, leftChild, node)
                # check if root was removed
                if node == self.root and node.numItems == 0:
                    self.root = leftChild

        else:
            if node.isLeaf() is False:
                child = self.getNextChild(key, node)
                leftSib, rightSib, parentLoc = self.getPrecSuccChild(child, node)

            else:
                child = node
                leftSib, rightSib, parentLoc = self.getPrecSuccChild(child, root)

            if child.numItems < child.minKey:
                if leftSib is not None and leftSib.numItems >= leftSib.minKey:
                    # get parent element
                    parentItem = node.removeItem(parentLoc)
                    # move an element from parent to child
                    child.insertItem(parentItem)
                    # move from sibling to parent
                    predChild = self.getPrecSuccChild(child, node)[0]
                    predKey = predChild.removeItem(predChild.numItems - 1)
                    self.moveChildren(predChild, child, isSucc = False)
                    node.insertItem(predKey)
                    # descend into child
                    self._delete(key, child, node)

                elif (rightSib is not None) and (rightSib.numItems >= rightSib.minKey):
                    # get parent of element
                    parentLoc = self.getParentPath(child, node, isSucc = True)[0]
                    parentItem = node.removeItem(parentLoc)
                    # move an element from parent to child
                    child.insertItem(parentItem)
                    # move from sibling to parent
                    succChild = self.getPrecSuccChild(child, node)[1]
                    succKey = succChild.removeItem(0)
                    self.moveChildren(succChild, child, isSucc = True)
                    node.insertItem(succKey)
                    # descend into child
                    self._delete(key, child, node)

                elif leftSib is not None and leftSib.numItems < leftSib.minKey:
                    # get parent item
                    parentItem = node.removeItem(parentLoc)
                    # merge left sibling into child node
                    self.mergeNodes(leftSib, child, node)
                    # insert parent into child
                    child.insertItem(parentItem)
                    # descend into child
                    self._delete(key, child, node)
                    # check if root was removed
                    if node == self.root and node.numItems == 0:
                        self.root = child

                elif rightSib is not None and rightSib.numItems < rightSib.minKey:
                    # get parent item
                    parentItem = node.removeItem(parentLoc)
                    # merge right sibling into child node
                    self.mergeNodes(rightSib, child, node)
                    # insert parent into child
                    child.insertItem(parentItem)
                    # descend into child
                    self._delete(key, child, node)
                    # check if root was removed
                    if node == self.root and node.numItems == 0:
                        self.root = child

            else:
                self._delete(key, child)

    def moveChildren(self, node1, node2, isSucc = True):
        if node1.isLeaf() is False:
            if isSucc is True:
                child = node1.disconnectChild(0, shift = 1)
                node2.connectChild(node2.numItems, child)
            else:
                child = node1.disconnectChild(node1.numItems + 1, shift = 1)
                node2.connectChild(0, child, shift = 1)






    def getPredKey(self, key, node, itemLoc):

        if node.isLeaf() is True:
            predKey = node.itemArray[node.numItems - 1]

        else:
            node = node.cArray[itemLoc]

            while node.isLeaf() is False:
                node = node.cArray[node.numItems]

            predKey = node.itemArray[node.numItems - 1]

        return predKey

    def getSuccKey(self, key, node, itemLoc):

        if node.isLeaf() is True:
            succKey = node.itemArray[0]

        else:
            succChild = node.cArray[itemLoc + 1]

            while succChild.isLeaf() is False:
                succChild = succChild.cArray[0]

            succKey = succChild.itemArray[0]

        return succKey

    def getPrecSuccChild(self, node, pNode, key=None):

        sibArray = pNode.cArray
        pLoc, nodeLoc = self.getParentPath(node, pNode)

        if ( nodeLoc > 0 ) and ( nodeLoc < ( node.order - 1 ) ):
            precChild = sibArray[nodeLoc - 1]
            succChild = sibArray[nodeLoc + 1]
        elif nodeLoc == 0:
            precChild = None
            succChild = sibArray[1]
        else:
            succChild = None
            precChild = sibArray[nodeLoc - 1]

        return precChild, succChild, pLoc


    def getParentPath( self, node, pNode, isSucc = False):
        pLoc = 0 #parent element
        cLoc = 0 #location of node in parent elements children

        # Node is not root
        if node.pNode is not None:
            if pNode is None:
                pNode = node.pNode
                cArray = node.pNode.cArray
            else:
                cArray = pNode.cArray

            foundParent = False
            i = 0

            while (i < len(cArray)) and (foundParent is False):
                child = cArray[i]

                if child == node:
                    cLoc = i
                    foundParent = True

                i += 1

            if cLoc > 0 and isSucc is False:
                pLoc = cLoc - 1
            else:
                pLoc = cLoc

        return pLoc, cLoc

    def remove(self, item, node, pNode):
        item = node.removeItem(item)

        if node.numItems == 0 and node.pNode is not None:
            nodeLoc = self.getParentPath(node, pNode)[1]
            pNode.disconnectChild(nodeLoc, shift = 1)

        return item


    def mergeNodes( self, node1, node2, pNode ):
        # node1 = from here
        # node2 - into here

        # Get number of children within each node
        num1 = node1._countChild()
        num2 = node2._countChild()

        # Merging smaller key node into larger key node
        if node1.itemArray[0].key < node2.itemArray[0].key:

            # if leaf, ignore children
            if node1.isLeaf() is False:
                for i in range(num2 - 1, -1, -1):
                    node2.cArray[i + num1] = node2.cArray[i]

                for j in range(num1):
                    node2.cArray[j] = node1.cArray[j]

            # move items from node1 into node2
            k = 0

            isEmpty = False
            while isEmpty is False:
                    item = self.remove(0, node1, pNode)
                    node2.insertItem(item)

                    if node1.numItems == 0:
                        isEmpty = True

        # Merging from larger key node into smaller key node
        else:
            idx = 0
            # move the children
            for l in range(num1, self.order):
                node2.cArray[l] = node1.cArray[idx]
                idx += 1

            # move the keys
            isEmpty = False
            while isEmpty is False:
                item = self.remove(0, node1, pNode)
                node2.insertItem(item)

                if node1.numItems == 0:
                    isEmpty = True

    def displayTree(self):
        self._recDisplayTree(self.root, 0, 0)
        print('-------------------------------------------')

    def _recDisplayTree(self, thisNode, level, cNum):
        print(f"level={level} child = {cNum}")
        thisNode._displayNode()

        numItems = thisNode.numItems

        i = 0
        isPrinted = False
        while i < numItems + 1 and isPrinted is False:
            nextNode = thisNode.cArray[i]
            if nextNode is not None:
                self._recDisplayTree(nextNode, level+1, i)
            else:
                isPrinted = True
            i += 1

    def balance( self ):
        # if 3 keys per node then a tree with 2 levels should have 3 + 3*4 nodes filled to be complete
        # if 3 keys and 3 levels then 3 + 3*4 + 3*4*4 and so on..
        numComplete = self.order - 1

        if self.ht == 0:
             balance = round((self.size / numComplete) * 100, 2)
        else:
            level = 1

            while level <= self.ht:
                numComplete += (self.order - 1)*(self.order)**level
                level += 1

            balance = round( (self.size / numComplete) * 100, 2)

        return balance

    def height(self):
        return self.ht

    def storeTree( self ):
        startT = timer()
        linkedList = dsaLL()

        for item in range(self.root.numItems + 1):
            self._storeTree(linkedList, self.root.cArray[item])

            if item < self.root.numItems:
                linkedList.insertLast(self.root.itemArray[item].value)

        elapsedT = timer() - startT
        self.sortTime += elapsedT
        return linkedList

    def _storeTree( self, llist, currNode ):
        if currNode is not None:
            if currNode.isLeaf() is True:
                for item in currNode:
                    if item is not None:
                        llist.insertLast(item)

            else:
                for i in range(currNode.numItems + 1):
                    child = currNode.cArray[i]
                    self._storeTree(llist, child)

    def __iter__(self):
        llist = self.storeTree()
        for share in llist:
            yield share


class Error( Exception ):
    pass


class TreeNodeError( Error ):
    """
    Exception called when attempting to perform an illegal operation
    on a tree node.

    Attributes:
        message --- explanation of the error
    """

class EmptyKeyTreeError( Error ):
    """
    Exception called when tree node is initialised with no value.

    Attributes:
        message --- explanation of the error
    """

class KeyNotFoundTreeError( Error ):
    """
    Exception called when tree node is not found.

    Attributes:
        message --- explanation of the error
    """
