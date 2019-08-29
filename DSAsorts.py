"""
Sort method containing bubble sort, insertion sort, selection sort, merge sort,
and quick sort algorithms.
"""
import numpy as np


class Sort:

    def bubbleSort(A):

        isSorted = False

        while isSorted is False:
            isSorted = True
            for i in range(0, len(A) - 1):
                if A[i] > A[i + 1]:
                    temp = A[i]
                    A[i] = A[i + 1]
                    A[i + 1] = temp
                    isSorted = False

    def insertionSort(A):

        for nn in range(1, len(A)):
            ii = nn

            temp = A[ii]
            while (ii > 0) and (A[ii - 1] > temp):

                A[ii] = A[ii - 1]
                ii = ii - 1

            A[ii] = temp

    def selectionSort(A):

        for n in range(0, len(A)):
            minIdx = n

            for i in range(n + 1, len(A)):
                if A[i] < A[minIdx]:
                    minIdx = i

            temp = A[minIdx]
            A[minIdx] = A[n]
            A[n] = temp

    @classmethod
    def mergeSort(cls, A):

        cls.__mergeSortRecurse(A, 0, len(A) - 1)

    @classmethod
    def __mergeSortRecurse(cls, A, leftIdx, rightIdx):

        if leftIdx < rightIdx:
            midIdx = (leftIdx + rightIdx) // 2

            cls.__mergeSortRecurse(A, leftIdx, midIdx)
            cls.__mergeSortRecurse(A, midIdx + 1, rightIdx)

            cls.__merge(A, leftIdx, midIdx, rightIdx)

    @classmethod
    def __merge(cls, A, leftIdx, midIdx, rightIdx):

        tempArr = np.zeros(rightIdx - leftIdx + 1, dtype=int)
        ii = leftIdx
        jj = midIdx + 1
        kk = 0

        while (ii <= midIdx) and (jj <= rightIdx):
            if A[ii] <= A[jj]:
                tempArr[kk] = A[ii]
                ii = ii + 1

            else:
                tempArr[kk] = A[jj]
                jj = jj + 1

            kk = kk + 1

        for ii in range(ii, midIdx + 1):
            tempArr[kk] = A[ii]
            kk = kk + 1

        for jj in range(jj, rightIdx + 1):
            tempArr[kk] = A[jj]
            kk = kk + 1

        for kk in range(leftIdx, rightIdx + 1):
            A[kk] = tempArr[kk - leftIdx]

    @classmethod
    def quickSort(cls, A):

        cls.__quickSortRecurse(A, 0, len(A) - 1)

    @classmethod
    def __quickSortRecurse(cls, A, leftIdx, rightIdx):

        if rightIdx > leftIdx:
            pivotIdx = (leftIdx + rightIdx) // 2
            newPivotIdx = cls.__doPartitioning(A, leftIdx, rightIdx, pivotIdx)

            cls.__quickSortRecurse(A, leftIdx, newPivotIdx - 1)
            cls.__quickSortRecurse(A, newPivotIdx + 1, rightIdx)

    @classmethod
    def __doPartitioning(cls, A, leftIdx, rightIdx, pivotIdx):

        pivotVal = A[pivotIdx]
        A[pivotIdx] = A[rightIdx]
        A[rightIdx] = pivotVal

        currIdx = leftIdx

        for ii in range(leftIdx, rightIdx):
            if A[ii] < pivotVal:
                temp = A[ii]
                A[ii] = A[currIdx]
                A[currIdx] = temp
                currIdx = currIdx + 1

        newPivotIdx = currIdx
        A[rightIdx] = A[newPivotIdx]
        A[newPivotIdx] = pivotVal

        return newPivotIdx
