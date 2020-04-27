
class Node:
    def __init__(self,value):
        self.__left = None
        self.__right = None
        self._value = value

    def getValue(self):
        return self._value

    def insertNode(self, value):
        if self._value:
            if value < self._value:
                if self.__left is None:
                    self.__left = Node(value)
                else:
                    self.__left.insertNode(value) #traverse down the left node and try to insert there.
            elif value > self._value:
                if self.__right is None:
                    self.__right = Node(value)
                else:
                    self.__right.insertNode(value) #traverse down the right node and try to insert there
            else:
                print("An error has occured ")
        else:
            self._value = value #root node case


    def InorderTraverse(self, root):
        result = ""
        if root is not None: #If there are still nodes to traverse
            result += self.InorderTraverse(root.__left)# left subtree traversal
            result += str(root._value) + ","
            result += self.InorderTraverse(root.__right) #right subtree traversal
        return result

    def PreorderTraverse(self,root):
        result = ""
        if root is not None: #If there are still nodes to traverse
            result += str(root._value) + ","
            result += self.PreorderTraverse(root.__left)#left subtree traversal
            result += self.PreorderTraverse(root.__right) #right subtree traversal
        return result

    def PostorderTraverse(self,root):
        result = ""
        if root is not None: #If there are still nodes to traverse
            result += self.PostorderTraverse(root.__left)#left subtree traversal
            result += self.PostorderTraverse(root.__right) #right subtree traversal
            result += str(root._value) + ","
        return result


