from heapq import heappush, heappop, heapify 
from CurrentSTate import currstate
import HelperFunctions as hf
import distutils

#Python code using Python libraries. Below Scratch implementation below
'''
# heappop - pop and return the smallest element from heap
# heappush - push the value item onto the heap, maintaining
#             heap invarient
# heapify - transform list into heap, in place, in linear time
  
# A class for Min Heap
class MinHeap:
      
    # Constructor to initialize a heap
    def __init__(self):
        self.heap = [] 
  
    def parent(self, i):
        return (i-1)/2
      
    # Inserts a new key 'k'
    def insertKey(self, k):
        heappush(self.heap, k)           
  
    # Decrease value of key at index 'i' to new_val
    # It is assumed that new_val is smaller than heap[i]
    def decreaseKey(self, i, new_val):
        self.heap[i]  = new_val 
        while(i != 0 and self.heap[self.parent(i)] > self.heap[i]):
            # Swap heap[i] with heap[parent(i)]
            self.heap[i] , self.heap[self.parent(i)] = (
            self.heap[self.parent(i)], self.heap[i])
              
    # Method to remove minium element from min heap
    def extractMin(self):
        return heappop(self.heap)
  
    # This functon deletes key at index i. It first reduces
    # value to minus infinite and then calls extractMin()
    def deleteKey(self, i):
        self.decreaseKey(i, float("-inf"))
        self.extractMin()
  
    # Get the minimum element from the heap
    def getMin(self):
        return self.heap[0]
  
# Driver pgoratm to test above function
heapObj = MinHeap()
heapObj.insertKey(3)
heapObj.insertKey(2)
heapObj.deleteKey(1)
heapObj.insertKey(15)
heapObj.insertKey(5)
heapObj.insertKey(4)
heapObj.insertKey(45)


print heapObj.extractMin(),
print heapObj.getMin(),
heapObj.decreaseKey(2, 1)
print heapObj.getMin()
'''

# compare the priority of two states by a specific sign
def comparePriority(s1: currstate, sign: str, s2: currstate, isLargerGFirst: bool):    
    if isLargerGFirst is True:
        # use tie breaker that prioritize the state with larger G value
        if sign == "==":
            return hf.bG(s1) == hf.bG(s2)
        elif sign == ">":
            return hf.bG(s1) > hf.bG(s2)
        elif sign == "<":
            return hf.bG(s1) < hf.bG(s2)
        elif sign == ">=":
            return hf.bG(s1) >= hf.bG(s2)
        elif sign == "<=":
            return hf.bG(s1) <= hf.bG(s2)
    else:
        # use tie breaker that prioritize the state with smaller G value
        if sign == "==":
            return hf.sG(s1) == hf.sG(s2)
        elif sign == ">":
            return hf.sG(s1) > hf.sG(s2)
        elif sign == "<":
            return hf.sG(s1) < hf.sG(s2)
        elif sign == ">=":
            return hf.sG(s1) >= hf.sG(s2)
        elif sign == "<=":
            return hf.sG(s1) <= hf.sG(s2)

class minheap(object):
    def __init__(self, isLargerGFirst: bool):
        self.data = []  # heap list
        self.count = len(self.data)  # number of elements
        self.isLargerGFirst = isLargerGFirst

    def size(self):
        return self.count

    def isEmpty(self):
        return self.count == 0

    def push(self, item):
        # insert item into heap
        self.data.append(item)
        self.count += 1
        self.shiftUp(self.count)

    def shiftUp(self, count):
        # Move state up to a proper location by priority to maintain the MinStateHeap
        while count > 1 and comparePriority(self.data[int(count / 2) - 1], ">", self.data[count - 1], self.isLargerGFirst):
            self.data[int(count / 2) - 1], self.data[count - 1] = self.data[count - 1], self.data[int(count / 2) - 1]
            count = int(count / 2)

    def peek(self):
        # Get the state with highest priority
        return self.data[0]

    def pop(self):
        # Pop the state with highest priority
        if self.count > 0:
            ret = self.data[0]
            self.data[0], self.data[self.count - 1] = self.data[self.count - 1], self.data[0]
            self.data.pop()
            self.count -= 1
            self.shiftDown(1)
            return ret

    def remove(self, state):
        # remove a specific state from heap
        if self.data.index(state) == 0:
            self.pop()
            return True
        else:
            if self.count > 0:
                while state in self.data:
                    stateIndex = self.data.index(state)
                    self.data[stateIndex], self.data[self.count - 1] = self.data[self.count - 1], self.data[stateIndex]
                    del (self.data[self.count - 1])
                    self.count -= 1
                    self.shiftDown(stateIndex + 1)
            else:
                return False

    def shiftDown(self, count):
        # Move state down to a proper location by priority to maintain the MinStateHeap
        while 2 * count <= self.count:
            # browse children
            j = 2 * count
            if j + 1 <= self.count:
                # browse right child
                if comparePriority(self.data[j], "<", self.data[j - 1], self.isLargerGFirst):
                    j += 1
            if comparePriority(self.data[count - 1], "<=", self.data[j - 1], self.isLargerGFirst):
                # if s than children, then break
                break
            self.data[count - 1], self.data[j - 1] = self.data[j - 1], self.data[count - 1]
            count = j

    def toString(self):
        result = "["
        for i in range(len(self.data)):
            result += ("%d: %s" % (hf.psG(self.data[i]), self.data[i].location))
            if i != len(self.data) - 1:
                result += ", "
        result += "]"
        return result

    def contains(self, s: currstate):
        if s in self.data:
            return True
        else:
            return False
