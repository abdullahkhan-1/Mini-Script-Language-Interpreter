class NumberNode:
    def __init__(self , value):
        self.value = value  # a python number (int or float)
        
class IfNode:
    def __init__(self , condition , body):
        self.condition = condition  # a CompareNode
        self.body = body  # a list of nodes to execute if the condition is true

class CompareNode:
    def __init__(self , left , op , right):
        self.left = left  # a node representing the left-hand side of the comparison
        self.op = op  # a string representing the comparison operator (e.g. '==', '!=', '<', '>', '<=', '>=')
        self.right = right  # a node representing the right-hand side of the comparison

class LetNode:
    def __init__(self , name , value):
        self.name = name  # a string representing the variable name
        self.value = value

class PrintNode:
    def __init__(self , value):  
        self.value = value  # a node representing the value to be printed (e.g. a StringNode, NumberNode, or IdentNode)

class IdentNode:
    def __init__(self , name):
        self.name = name  # a string representing the variable name

class StringNode:
    def __init__(self , value):
        self.value = value  # a python string

class BinOpNode:
    def __init__(self , left , op , right):
        self.left = left  # a node representing the left-hand side of the binary operation
        self.op = op  # a string representing the binary operator (e.g. '+', '-', '*', '/')
        self.right = right  # a node representing the right-hand side of the binary operation

class WhileNode:
    def __init__(self , condition , body):
        self.condition = condition  # a CompareNode representing the loop condition
        self.body = body  # a list of nodes to execute in the loop body

class AssignNode:
    def __init__(self , name , value):
        self.name = name  # a string representing the variable name
        self.value = value  # a node representing the value to be assigned
