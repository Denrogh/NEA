"""Python file that contains all the conversion methods, postfix to infix, infix to postfix, posteval, infixeval and the stack and queue class."""
import random
class Stack:
    def __init__(self):
        self.__items = []

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        if len(self.__items) >= 1:
            return self.__items.pop() #Will pop off the top of the stack
        else:
            raise IndexError("this is an empty stack, cannot be poped from")

    def top(self):
        if len(self.__items) >= 1:
            return self.__items[-1] #Shows the top value of the stack
        else:
            raise IndexError("There is no top to an empty stack!")

    def size(self):
        return len(self.__items) # Returns the number of items in the stack

class Queue:
    def __init__(self):
        self.__items = []

    def enqueue(self, item):
        self.__items.insert(0 ,item) #Pushes item to the back of the queue

    def dequeue(self):
        if len(self.__items) >= 1:
            return self.__items.pop() #Removes item at front of queue
        else:
            raise IndexError("This queue is empty")

    def size(self):
        return len(self.__items) #Returns number of items in the queue

    #def print_queue(self):
        #return self.__items

def operator(char):
    operators = ["/","^","*","+","-","(",")"]
    if char in operators:
        return True
    return False

def priority(operator):
    if operator == '^':
        return 5
    if operator == '/' or operator == '*':
        return 4
    if operator == '+' or operator == '-':
        return 2
    if operator == ')' or operator == '(':
        return 1
    else:
        raise ValueError("this is not a valid operator")

def compute_operator(a,b, operator):
    if operator == '+':
        return a + b
    if operator == '-':
        return a - b
    if operator == '*':
        return a * b
    if operator == '/':
        return a // b
    if operator == '^':
        return pow(a,b)
    else:
        return ValueError("invalid operator to apply")

def generate_postfix():
    char_set = "1234567890+-/*^" #allowed charcater set
    length = random.randint(5,12) #Strings of right length
    postfix = ""
    for _ in range(length):
        index = random.randint(0,14) #picks a random character out of char set
        postfix += char_set[index]
    return postfix

def check_postfix(postfix):
    try:
        post_sum = postfix_evaluation(postfix) #postfix_sum evaluation
        infix = postfix_to_infix(postfix) #infix conversion
        infix_sum = infix_evaluation(infix) #infix_sum evaluation
        if post_sum == infix_sum:
            return True
    except:
        #if an error happens at any point it is not a valid postfix
        return False

def check_infix(infix):
    try:
        infix_sum = infix_evaluation(infix)
        postfix = infix_to_postfix(infix)
        postfix_sum = postfix_evaluation(postfix)
        if infix_sum == postfix_sum:
            return True
    except:
        return False

def random_postfix():
    postfix_array = []
    for i in range(20):
        check = False
        while not check:
            postfix = generate_postfix() #Gives a random possibly postfix string
            check = check_postfix(postfix) #Checks if it is postfix
        postfix_array.append(postfix)#If it is postfix appended to array
    return postfix_array

def random_infix(postfix_array):
    infix_array = []
    for i in postfix_array:
        infix_array.append(postfix_to_infix(i))
    return infix_array

################################################################################################################

def postfix_to_infix(postfix):
    OutStack = Stack() #Initialise Stack and Queue
    OutputQueue = Queue()
    postfix = list(postfix) #Allows string to be looped through
    infix = ""
    for char in postfix:
        if not operator(char):
            OutStack.push(char) #If the character is not an operator (a number) push onto the array
        else:
            operand1 = OutStack.pop() #Pop off two operand
            operand2 = OutStack.pop() #Not necessarily operand, might be an expression like (A+B)
            OutStack.push("(" + operand2 + char + operand1 + ")") #Push them onto the stack and add brackets, giving them order
    OutputQueue.enqueue(OutStack.pop()) #Pops the stack, returning the infix string
    while (OutputQueue.size() > 0):
        infix += OutputQueue.dequeue()
    infix = infix[1:-1] #Removes outermost brackets from expression
    return infix

################################################################################################################

def infix_to_postfix(infix):
    OperatorStack = Stack() #Initialise Stack and Queue
    OutputQueue = Queue()
    infix = list(infix)
    postfix = ""
    for token in infix:
        if not operator(token): #token is an operand
            OutputQueue.enqueue(token) #push into output queue
        elif token =='(':  #left paranthesis case
            OperatorStack.push(token)
        elif token == ')': #right paranthesis case
            while True:
                temp_token = OperatorStack.pop() #Tokens will keep on being popped until a closing right bracket is found
                if temp_token is None or temp_token == '(':
                    break #Escapes while loop
                elif operator(temp_token): #Left paranthesis not found, pop from Operator stack and enqueue operator into output queue
                    OutputQueue.enqueue(temp_token)
        else:
            if OperatorStack.size() > 0: #Whilst the operator stack still has tokens
                top_token = OperatorStack.top()
                while (OperatorStack.size() > 0) and (priority(top_token) >= priority(token)): #stack is not empty and priorities are correct
                    OutputQueue.enqueue(OperatorStack.pop())
                    top_token = OperatorStack.top() #Sets the top_token to the new top of the operator stack
            OperatorStack.push(token)
    #Conversion Complete, processing results
    while (OperatorStack.size() > 0): #Emptying Operator stack for leftover operators
        OutputQueue.enqueue(OperatorStack.pop())
    while (OutputQueue.size() > 0): #Processing OutputQueue into a string
        postfix += OutputQueue.dequeue()
    return postfix

################################################################################################################

def postfix_evaluation(postfix):
    EvalStack= Stack()
    for token in postfix:
        #print(EvalStack.print_stack(),"printing whole stack")
        if operator(token):
            if token == '+':
                char1 = int(EvalStack.top())
                EvalStack.pop()
                char2 = int(EvalStack.top())
                EvalStack.pop()
                EvalStack.push(char1+char2)
                #print("char1+char2",char1,char2)
            if token == '*':
                char1 = int(EvalStack.top())
                EvalStack.pop()
                char2 = int(EvalStack.top())
                EvalStack.pop()
                EvalStack.push(char1*char2)
                #print("char1*char2",char1,char2)
            if token == '-':
                char1 = int(EvalStack.top())
                EvalStack.pop()
                char2 = int(EvalStack.top())
                EvalStack.pop()
                EvalStack.push(char2-char1)
                #print("char1-char2",char1,char2)
            if token == '/':
                char1 = int(EvalStack.top())
                EvalStack.pop()
                char2 = int(EvalStack.top())
                EvalStack.pop()
                EvalStack.push(char2//char1)
                #print("char1+char2",char1,char2)
            if token == '^':
                char1 = int(EvalStack.top())
                EvalStack.pop()
                char2 = int(EvalStack.top())
                EvalStack.pop()
                EvalStack.push(char1^char2)
        else:
            EvalStack.push(token)
            #print(token, "pushed token")
    if EvalStack.size() == 1:
        return EvalStack.pop()
    else:
        return ValueError("This is not a postfix expression")
##############################################################################################

def infix_evaluation(infix):
    ValueStack = Stack()
    OperatorStack = Stack()
    index = 0
    while index < len(infix):
        if infix[index] == '(':
            OperatorStack.push(infix[index])
            index += 1
        elif infix[index] == ')':
            while (OperatorStack.size() > 0) and (OperatorStack.top() != '('):
                value2 = ValueStack.pop()
                value1 = ValueStack.pop()
                op = OperatorStack.pop()
                ValueStack.push(compute_operator(value1, value2, op))
            OperatorStack.pop()
            index += 1
        elif not operator(infix[index]):  # if the token is a digit
            sum = 0
            while index < len(infix) and (not (operator(infix[index]))):
                sum = (sum * 10) + int(infix[index])
                index += 1
            ValueStack.push(sum)
        else:  # if the token is an operator
            while (OperatorStack.size() > 0) and (priority(OperatorStack.top()) >= priority(infix[index])):
                value2 = ValueStack.pop()
                value1 = ValueStack.pop()
                op = OperatorStack.pop()
                ValueStack.push(compute_operator(value1, value2, op))
            OperatorStack.push(infix[index])
            index += 1

    while OperatorStack.size() > 0: ##Applying all leftover operators
        value2 = ValueStack.pop()
        value1 = ValueStack.pop()
        op = OperatorStack.pop()
        #print("value2,value1,operator", value2, value1, operator)
        ValueStack.push(compute_operator(value1, value2, op))
    return ValueStack.top() # The top of the value stack (or alternatively the only value in the value stack will return
                            #the value of the expression

#######################################################################################################################

#print(postfix_to_infix("549++"),"Expecting 5+(4+9)")
#print(postfix_to_infix("23*8+"), "Expecting (2*3)+8")
#print(postfix_to_infix("ABC/-AK/L-*"), "Expecting (A-(B/C))*((A/K)-L)")
#print(postfix_to_infix("ABC-+DE-FG-H+/*"), "Expecting (A+(B-C))*((D-E)/((F-G)+H))")


#print(infix_to_postfix("5+(4+9)"), "Expecting (549++)")
#print(infix_to_postfix("(2*3)+8"), "Expecting (23*8+)")
#print(infix_to_postfix("(A-(B/C))*((A/K)-L)"), "Expecting (ABC/-AK/L-*)")
#print(infix_to_postfix("(A+(B-C))*((D-E)/((F-G)+H))"), "Expecting (ABC-+DE-FG-H+/*)")

##tests from http://www.cs.csi.cuny.edu/~zelikovi/csc326/data/assignment5.htm
print(postfix_evaluation("4572+-*"), """Expected output: -16""")
print(postfix_evaluation("34+2*7/"), """Expected output: 2""")
print(postfix_evaluation("45+"), """Expected output: 9""")
print(postfix_evaluation("45+72-*"), """Expected output: 45""")
print(postfix_evaluation("57+62-*"), """Expected output: 48""")
print(postfix_evaluation("42351-+*+"), """Expected output: 18""")
print(postfix_evaluation("42+351-*+"), """Expected output: 18""")






#print(infix_evaluation("4+5")), """Expected output 9"""
#print(infix_evaluation("3+5+7")), """Expected output 15"""
#print(infix_evaluation("7+5-7")), """Expected output 5"""
#print(infix_evaluation("(3+6)*3")), """Expected output 27"""
#print(infix_evaluation("((4/2)*5)+5")), """Expected output 15"""
#print(infix_evaluation("4-(6*(5-2))+3")), """Expected output -11"""
