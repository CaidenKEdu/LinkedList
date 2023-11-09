class Node:
    def __init__(self, val=None):
        if val != None:
            self.val = val
            self.next = Node()
        else:
            self.val = None
            self.next = None
    def append(self, val):
        if self.val != None:
            self.next.append(val)
        else:
            self.val = val
            self.next = Node()
    def __str__(self):
        if self.val != None:
            outString = str(self.val)
            outString += ", "
            outString += str(self.next)
            return outString
        else:
            return ''


def main():
    myList = Node()
    myList.append(1)
    myList.append(2)
    myList.append(3)
    print(myList)


if __name__ == "__main__":
    main()