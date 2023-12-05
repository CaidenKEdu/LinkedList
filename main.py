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

    def maxIdx(self):
        if self.isSorted() == True:
            return (self.len - 1)
        else:
            if self.getListType() == 'int':
                largest = self[0]
                for i in range(self.len-1):
                    if largest < self[i + 1]:
                        largest = self[i + 1]
                return self.find(largest)
            elif self.getListType() == 'str':
                largest = self[0]
                for i in range(self.len-1):
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
                    if len(largest) > len(self[i + 1]):
                        largest = self[i + 1]
                return self.find(largest)
            else:
                raise TypeError("Objects In List Are Not Sortable")

    def find(self, value):
        for i in range(self.len):
            if self[i] == value:
                return i
        return None

def main():
    mylist1 = LinkedList([1, 2, 3, 4, 5])
    print(mylist1.minIdx())




if __name__ == '__main__':
    main()