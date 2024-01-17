import random
from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib import animation
sys.setrecursionlimit(10000000)

class Node:
    def __init__(self, val=None):
        if val is not None:
            self.value = val
            self.next = Node()
        else:
            self.value = None
            self.next = None

    def append(self, val):
        if self.value is not None:
            self.next.append(val)
        else:
            self.value = val
            self.next = Node()

    def __str__(self):
        return str(self.value)

class LinkedList:
    def __init__(self, values):
        self.head = Node()
        self.curr = self.head
        self.len = 0
        try:
            self.concat(values)
        except TypeError:
            self.append(values)

    def append(self, val):
        self.len += 1
        self.head.append(val)

    def concat(self, values):
        for item in values:
            self.append(item)

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr.value is not None:
            out = self.curr.value
            self.curr = self.curr.next
            return out
        else:
            self.curr = self.head
            raise StopIteration

    def __str__(self):
        out = '['
        for item in self:
            out += str(item) + ', '
        return out[:-2] + ']'

    def __len__(self):
        return self.len

    def __getitem__(self, item):
        if item in range(-self.len, self.len):
            curr = self.head
            item %= self.len
            for _ in range(item):
                curr = curr.next
            return curr.value
        else:
            raise IndexError(f'Index {item} is out of range for list of length {self.len}.')

    def __setitem__(self, key, value):
        if key in range(-self.len, self.len):
            curr = self.head
            key %= self.len
            for _ in range(key):
                curr = curr.next
            curr.value = value
        else:
            raise IndexError(f'Index {key} is out of range for list of length {self.len}.')

    def __delitem__(self, key):
        if key in range(-self.len, self.len):
            curr = self.head
            key %= self.len
            for i in range(self.len):
                if i < key:
                    curr = curr.next
                elif i < self.len - 1:
                    curr = curr.next
                    self[i] = curr.value
                else:
                    self[i] = None
                    self.len -= 1
        else:
            raise IndexError(f'Index {key} is out of range for list of length {self.len}.')

    def insert(self, key, item):
        if key in range(-self.len, self.len):
            self.append(self[self.len - 1])
            curr = self.head
            key %= self.len
            for i in range(self.len):
                if i < key:
                    curr = curr.next
                elif i == key:
                    temp2 = 0
                    temp = self[i]
                    self[i] = item
                elif i <= self.len:
                    temp2 = temp
                    temp = self[i]
                    self[i] = temp2
        else:
            raise IndexError(f'Index {key} is out of range for list of length {self.len}.')

    def swap(self, a, b):
        prev = self[a]
        self[a] = self[b]
        self[b] = prev

    def getListType(self):
        temp = 0
        for i in self:
            if type(i) == int:
                if temp == 0:
                    temp = 0
                else:
                    temp = 2
                    break
            elif type(i) == str:
                if i == self[0]:
                    temp = 1
                elif temp == 1:
                    temp = 1
                else:
                    temp = 2
                    break
            else:
                temp = 2
                break
        if temp == 0:
            return 'int'
        elif temp == 1:
            return 'str'
        else:
            return 'mix'

    def isSorted(self):
        if self.getListType() == 'int':
            temp = 0
            for i in range(self.len-1):
                if self[i] <= self[i+1]:
                    temp = 0
                else:
                    temp = 1
                    break
            if temp == 0:
                return True
            else:
                return False
        elif self.getListType() == 'str':
            temp = 0
            for i in range(self.len-1):
                if len(self[i]) <= len(self[i + 1]):
                    temp = 0
                else:
                    temp = 1
                    break
            if temp == 0:
                return True
            else:
                return False
        else:
            raise TypeError("Objects In List Are Not Sortable")

    def maxIdx(self, lim):
        if self.isSorted() == True:
            return lim
        else:
            if self.getListType() == 'int':
                largest = self[0]
                for i in range(lim):
                    if largest < self[i + 1]:
                        largest = self[i + 1]
                return self.find(largest)
            elif self.getListType() == 'str':
                largest = self[0]
                for i in range(lim):
                    if len(largest) < len(self[i + 1]):
                        largest = self[i + 1]
                return self.find(largest)
            else:
                raise TypeError("Objects In List Are Not Sortable")

    def minIdx(self):
        if self.isSorted() == True:
            return 0
        else:
            if self.getListType() == 'int':
                largest = self[0]
                for i in range(self.len-1):
                    if largest > self[i + 1]:
                        largest = self[i + 1]
                return self.find(largest)
            elif self.getListType() == 'str':
                largest = self[0]
                for i in range(self.len-1):
                    if largest > self[i + 1]:
                        largest = self[i + 1]
                return self.find(largest)
            else:
                raise TypeError("Objects In List Are Not Sortable")

    def find(self, value):
        for i in range(self.len):
            if self[i] == value:
                return i
        return None

    def fill(self, int):
        for i in range(int):
            self.append(i+1)

    def convert(self):
        list = []
        for i in self:
            list.append(i)
        return list

    def sort1(self): #, artists, ax, y
        steps = 0
        while self.isSorted() == False:
            for i in range(self.len - 1):
                if self[i] > self[i+1]:
                    self.swap(i, i+1)
            # container = ax.bar(y, self.convert(), color='tab:blue')
            # artists.append(container)
            steps += 1
            print(steps)
        # return steps

    def sort2(self):
        steps = 0
        while self.isSorted() == False:
            for x in range(int(np.emath.log2(self.len))-1):
                for i in range((2**x)-1, self.len, 2**(x+1)):
                    if self[i] > self[i+(2**x)]:
                        for j in range(2**x):
                            self.swap(i-j, i+(2**x)-j)
            for i in range(self.len-3):
                if self[i] > self[i+2]:
                    self.swap(i, i+2)
            for i in range(1, self.len-1, 2):
                if self[i] > self[i+1]:
                    self.swap(i, i + 1)
            steps += 1
            print(steps)

    def sort3(self):
        steps = 0
        for i in range(self.len-1):
            self.swap(self.maxIdx(self.len-1-i), self.len-1-i)
            steps += 1
            print(steps)

    def sort4(self):
        self.swap(self.maxIdx(self.len - 1), self.find(self[-1]))
        for i in range(2**7):
            for j in range(self.len-i-1):
                if self[j] > self[j + i]:
                    self.swap(j, j + i)
            print(2**7-i)
        for j in range(2**7):
            for i in range(self.len-1):
                if self[i] > self[i+1]:
                    self.swap(i, i+1)
            print(2 ** 7 - j)

    def sort5(self):
        for j in range(self.len//32):
            for i in range(self.len-j-1):
                if self[i] > self[i+j+1]:
                    self.swap(i, i+j+1)
            print(self.len//32-j)

        while self.isSorted() == False:
            for i in range(self.len-1):
                if self[i] > self[i+1]:
                    self.swap(i, i+1)
                print("Cleaning")

    def bubbleSort(self):
        while self.isSorted() == False:
            for i in range(self.len-1):
                if self[i] > self[i+1]:
                    self.swap(i, i+1)

    def mergeSort(self): #does not work
        if self.len == 1:
            return self
        else:
            List = LinkedList([])
            list1 = LinkedList([])
            list2 = LinkedList([])
            list1Temp = 0
            list2Temp = 0
            listNumber = int(self.len / 2) - 1
            print(self)
            for i, item in enumerate(self):
                if i <= listNumber:
                    list1.append(item)
                else:
                    list2.append(item)
            list1 = list1.mergeSort()
            list2 = list2.mergeSort()
            while list1Temp <= listNumber - 1 and list2Temp <= self.len - listNumber - 1:
                if list1[list1Temp] > list2[list2Temp]:
                    List.append(list2[list2Temp])
                    list2Temp += 1
                else:
                    List.append(list1[list1Temp])
                    list1Temp += 1
            else:
                if list1Temp > listNumber:
                    for j in range((self.len-listNumber)-list2Temp - 1):
                        List.append(list2[j+list2Temp])
                elif list2Temp > self.len - listNumber:
                    for j in range(listNumber-list1Temp - 1):
                        List.append(list1[j + list1Temp])
            return List

    def mergeSort2(self):
        if self.len == 1:
            return self
        else:
            List = LinkedList([])
            listFront = LinkedList([])
            listBack = LinkedList([])
            middleIdx = (self.len//2) - 1
            for i in range(self.len):
                if i <= middleIdx:
                    listFront.append(self[i])
                else:
                    listBack.append(self[i])
            listFront = listFront.mergeSort2()
            listBack = listBack.mergeSort2()
            while listFront.len > 0 and listBack.len > 0:
                if listFront[0] > listBack[0]:
                    List.append(listBack[0])
                    del listBack[0]
                else:
                    List.append(listFront[0])
                    del listFront[0]
            else:
                if listFront.len == 0:
                    for i in listBack:
                        List.append(i)
                else:
                    for i in listFront:
                        List.append(i)
            return List

    def bogoSort(self):
        while self.isSorted() == False:
            for i in range(self.len*10):
                self.swap(random.randint(0, self.len-1), random.randint(0, self.len-1))
            print(self)

    def quickSort(self):
        if self.len == 0:
            return LinkedList([])
        elif self.len == 1:
            return self
        else:
            listFront = LinkedList([])
            listBack = LinkedList([])
            for i in self:
                if self[-1] <= i:
                    listBack.append(i)
                else:
                    listFront.append(i)
            del listBack[-1]
            listFront = listFront.quickSort()
            listBack = listBack.quickSort()
            listFront.append(self[-1])
            for i in listBack:
                listFront.append(i)
            return listFront

    def fillReverse(self, n):
        for i in range(n):
            self.append(n-i)

    def clear(self):
        for i in range(self.len):
            del self[0]

    def sortedIdx(self):
        n = 1
        prev = self[0]
        for i, val in enumerate(self):
            if val > prev:
                n += 1
            prev = val
        return n/self.len

    def comboSort(self):
        if self.sortedIdx() > 0.9 or self.sortedIdx() < 0.1:
            print("Merge Activating!")
            return self.mergeSort2()
        else:
            print("Quick Activating!")
            return self.quickSort()

def main():
    '''
    n = 1000
    mylist1 = LinkedList([])
    mylist1.fill(n)
    for i in range(10000):
        mylist1.swap(random.randint(0, n - 1), random.randint(0, n - 1))
    print(mylist1)
    print(f'Sorted Index: {mylist1.sortedIdx()}')
    time = perf_counter()
    mylist = mylist1.comboSort()
    time = perf_counter() - time
    print(mylist)
    print(f'Sorted Index: {mylist.sortedIdx()}')
    print(f"Is Sorted?: {mylist.isSorted()}")
    print(f"Seconds: {time} s")
    fig, ax = plt.subplots()
    number = 500
    timeList = []
    for n in range(1, number + 1):
        mylist1 = LinkedList([])
        mylist1.fill(n)
        for i in range(10000):
            mylist1.swap(random.randint(0, n - 1), random.randint(0, n - 1))
        #print(mylist1)
        time = perf_counter()
        mylist = mylist1.quickSort()
        time = perf_counter() - time
        #print(mylist)
        #print(f"{time} Seconds")
        #print(f"Is Sorted?: {mylist.isSorted()}")
        timeList.append(time)
        print(n)
    x = []
    for i in range(1, number + 1):
        x.append(i)
    ax.plot(x, timeList)
    plt.show()
    fig, ax = plt.subplots()
    artists = []
    mylist1 = LinkedList([])
    n = 10
    mylist1.fill(2 ** n)
    y = range(mylist1.len)
    for i in range(10000):
        mylist1.swap(random.randint(0, (2 ** n) - 1), random.randint(0, (2 ** n) - 1))
    print(mylist1)
    time = perf_counter()
    steps = mylist1.sort5(artists, ax, y)
    time = perf_counter() - time
    print(time)
    print(mylist1)
    print(steps)
    print(mylist1.isSorted())
    ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=steps)
    ani.save(filename="sort3.gif", writer="pillow")
    '''
    fig, ax = plt.subplots()
    n = 500
    time = []
    for i in range(1, n):
        mylist1 = LinkedList([])
        mylist1.fill(i)
        for _ in range(2000):
            mylist1.swap(random.randint(0, (i) - 1), random.randint(0, (i) - 1))
        timeTemp = perf_counter()
        mylist1 = mylist1.quickSort()
        timeTemp = perf_counter() - timeTemp
        time.append(timeTemp)
        print(i)
    x = []
    for i in range(1, n):
        x.append(i)
    ax.plot(x, time, label='Shuffled')
    time2 = []
    for i in range(1, n):
        mylist1 = LinkedList([])
        mylist1.fill(i)
        for _ in range(10):
            mylist1.swap(random.randint(0, (i) - 1), random.randint(0, (i) - 1))
        timeTemp = perf_counter()
        mylist1 = mylist1.quickSort()
        timeTemp = perf_counter() - timeTemp
        time2.append(timeTemp)
        print(i)
    time3 = []
    ax.plot(x, time2, label='Little Mixing')
    for i in range(1, n):
        mylist1 = LinkedList([])
        mylist1.fill(i)
        # for _ in range(2000):
        # mylist1.swap(random.randint(0, (i) - 1), random.randint(0, (i) - 1))
        timeTemp = perf_counter()
        mylist1 = mylist1.quickSort()
        timeTemp = perf_counter() - timeTemp
        time3.append(timeTemp)
        print(i)
    ax.plot(x, time3, label='No Mixing')
    ax.legend()
    plt.show()

if __name__ == '__main__':
    main()