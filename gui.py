import pygame
from database import *
from conversion import *
from tree import *


class Button:
    def __init__(self,menu,action,width,height,colour,boxColour,font_size,text,x,y):
        self.__menu = menu #the menu it is being used in
        self.__action = action #what the button does
        self.__width = width
        self.__height = height
        self.__colour = colour
        self.__boxColour = boxColour
        self.__text = text
        self.__x = x
        self.__y = y
        self.surface = pygame.Surface((width,height)) #the surface object of the button
        self.__font_size = font_size
        self.__font = pygame.font.SysFont("tahoma",self.__font_size)
        self.__boxColourOriginal = boxColour
        self.drawButton()

    def getAction(self):
        return self.__action

    def onButton(self,pos):
        if pos[0] > (self.__x - (self.__width/2)) and pos[0] < (self.__x + (self.__width/2)):
            if pos[1] > (self.__y - (self.__height/2)) and pos[1] < (self.__y + (self.__height/2)):
                self.__boxColour = black
                return True
        self.__boxColour = self.__boxColourOriginal
        return False

    def __insertText(self):
        text_render = self.__font.render(self.__text, 1, self.__colour)  # renders font/text
        text_render_size = self.__font.size(self.__text)
        x_config = text_render_size[0]/2
        y_config = text_render_size[1]/2
        self.surface.blit(text_render, ((self.surface.get_width()/2 - x_config), (self.surface.get_height()/2 - y_config)))  # This draws the text to the right place

    def drawButton(self):
        self.surface.fill(self.__boxColour)
        self.__insertText()
        self.__menu.surface.blit(self.surface,(self.__x - (self.__width / 2) , self.__y - (self.__height / 2)))

class InputBox:
    def __init__(self, menu,number,charSet,x,y,width,height,text="",):
        self.__menu = menu
        self.__number = number #this is only used if there are multiple boxes
        self.__colourInactive = red
        self.__colourActive = white
        self.__colour = self.__colourInactive
        self.__Rect = pygame.Rect(x,y,width,height)
        self.__font = pygame.font.SysFont('tahoma',30)
        self.__text = text
        self.__textSurface = self.__font.render(text, True, self.__colour)
        self.__active = False
        self.__UpdateBox()
        if charSet == "all":
            self.__characters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890#?!@$%^&*=+<>")
        else:
            self.__characters = ["0","1","2","3","4","5","6","7","8","9","+","-","/","^","*","(",")"]

    def clickEvent(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.__Rect.collidepoint(mouse_pos[0],mouse_pos[1]):
            self.__active = not self.__active
        else:
            self.__active = False
        self.__colour = self.__colourActive if self.__active else self.__colourInactive
        return self.__active

    def typeEvent(self,event):
        inputText = None
        self.clickEvent()
        if event.type == pygame.KEYDOWN:
            if self.__active:
                if event.key == pygame.K_BACKSPACE:
                    self.__text = self.__text[:-1] #remove the last inputted character
                elif event.unicode in self.__characters and (len(self.__text) <= 23):
                    self.__text += event.unicode #add allowed characters to text
                elif event.key == pygame.K_RETURN:
                    value = self.__text
                    self.__text = ''
                    self.__textSurface = self.__font.render(self.__text, True, self.__colour)
                    return value
                self.__textSurface = self.__font.render(self.__text, True, self.__colour)
                inputText = True
        return inputText

    def getNumber(self):
        return self.__number

    def __UpdateBox(self):
        Width = max(400, self.__textSurface.get_width() + 10)
        self.__Rect.width = Width

    def drawBox(self):
        self.__UpdateBox()
        self.__menu.surface.blit(self.__textSurface,(self.__Rect.x, self.__Rect.y))
        pygame.draw.rect(self.__menu.surface, self.__colour, self.__Rect, 2)

class VisualNode(Node):
    def __init__(self,menu,value,x,y):
        super().__init__(value)
        self.__value = super().getValue() #Gets value of node
        self.__menu = menu #Gives menu it belongs to
        self.__colour = red #Base colour of node
        self.__x = x
        self.__y = y #Co-ordinates
        self.__radius = 40 #Fixed radius
        self.__font = pygame.font.SysFont('tahoma',30)
        self.surface = pygame.Surface((width,height)) #the surface object of the button

    def visitNode(self): #Used during traversal to visit nodes and change their colour
        self.__colour = green

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def __insertValue(self):
        text_render = self.__font.render(self.__value, 1, red) # renders font/text
        self.__menu.surface.blit(text_render,(self.__x-7.5,self.__y-15))

    def drawNode(self):
        self.__insertValue()
        pygame.draw.circle(self.__menu.surface, self.__colour, (self.__x, self.__y), self.__radius, 2)

    def connectNodes(self,node1,node2):
        node1_centre = ((node1.getX() , node1.getY()))
        node2_centre = ((node2.getX(),node2.getY()))
        pygame.draw.line(self.__menu.surface,red,(node1_centre),(node2_centre))




class Menu:
    """Base Menu Object"""

    def __init__(self,screen,title,titleColour):
        self.__screen = screen
        self.__title = title
        self.__titleColour = titleColour
        self.surface = pygame.Surface((width,height))
        self.__buttons = [] #Stores all button objects
        self.__input = [] #Stores all input boxes
        self.__nodes = [] #Stoes all visual node objects

    def addButton(self,action,width,height,colour,boxColour,font_size,text,x,y):
        newButton = Button(self,action,width,height,colour,boxColour,font_size,text,x,y)
        self.__buttons.append(newButton)

    def addInput(self,number,charSet,x,y,width,height):
        newInputBox = InputBox(self,number,charSet,x,y,width,height)
        self.__input.append(newInputBox)

    def addNode(self,value,x,y):
        newNode = VisualNode(self,value,x,y)
        self.__nodes.append(newNode)

    def visitNode(self,index):
        node = self.__nodes[index]
        node.visitNode()

    def assignBox(self, number):
        box = self.__input[number]
        return box

    def buttonClick(self, mouse_pos):
        for button in self.__buttons:
            if button.onButton(mouse_pos):
                return button.getAction()
        return None

    def InputClick(self):
        for box in self.__input:
            if box.clickEvent(): #if the box was clicked retrieve its number so it can be used
                return box.getNumber()
        return None

    def drawText(self,text,x,y,colour,size):
        font = pygame.font.SysFont("tahoma", size)
        text = font.render(text, 1, colour)
        self.surface.blit(text,(x,y))
        self.__screen.blit(self.surface,(0,0))


    def drawMenu(self):
        self.surface.fill(black)
        font = pygame.font.SysFont("tahoma",60)
        title = font.render(self.__title,1,self.__titleColour)
        render_size = font.size(self.__title)
        #Adjust x and y to top middle of screen
        x_config = render_size[0]/2
        y_config = render_size[1]/2
        x = (width/2) - x_config
        y = (height/8) - y_config
        #'print' to screen
        self.surface.blit(title,(x,y))
        ##Printing Buttons
        pos = pygame.mouse.get_pos()
        for button in self.__buttons:
            button.onButton(pos)
            button.drawButton()
        for inputBox in self.__input:
            inputBox.clickEvent()
            #inputBox.typeEvent(event)
            inputBox.drawBox()
        for nodes in self.__nodes:
            nodes.drawNode()
            nodes.connectNodes(self.__nodes[0],self.__nodes[1])
            nodes.connectNodes(self.__nodes[1],self.__nodes[2])
            nodes.connectNodes(self.__nodes[1],self.__nodes[3])
            nodes.connectNodes(self.__nodes[3],self.__nodes[4])
            nodes.connectNodes(self.__nodes[0],self.__nodes[5])
            nodes.connectNodes(self.__nodes[5],self.__nodes[6])
            nodes.connectNodes(self.__nodes[5],self.__nodes[7])
        self.__screen.blit(self.surface,(0,0))

##Global constants
white = (255,255,255)
black = (0,0,0)
red  = (255,0,0)
green = (63,122,77)
blue = (15,82,186)
s_blue = (29,41,81)
grey = (10,10,10)
width = 1366
height = 768

def quit_program():
    pygame.display.quit()
    pygame.quit()
    exit()

def GraphicalInterface():

    #initialize() #Intialises Database
    pygame.init()
    pygame.display.set_caption('Tree Traversal Algorithms')
    screen = pygame.display.set_mode((width,height)) #sets up a fullscreen program
    screen.fill(black) #set background to black

    #Setting up the unique menus.
    #Sign Up menu
    SignUp = Menu(screen, "Sign Up", red)
    SignUp.addButton("Sign Up",200,100,red,grey,48,"Sign Up", (width/5),(1.75*height/2))
    SignUp.addButton("SignLogin",400,100,red,grey,24,"Already have an account? Login",(4*width/5),(1.75*height/2))
    SignUp.addInput(0, "all", (0.7*width/2), (1.5*height/5), 200, 50)  # username box
    SignUp.addInput(1, "all", (0.7*width/2), (3.5*height/5.5), 200, 50)  # password box


    #Login Menu
    Login = Menu(screen,"Login", red)
    Login.addButton("Login",200,100,red,grey,72,"Login",(width/5),(1.75*height/2))
    Login.addButton("SignUpBack",300,100,red,grey,24,"No account? Sign Up",(4*width/5),(1.75*height/2))
    Login.addInput(0, "all", (0.7*width/2), (1.5*height/5), 200, 50)  # username box
    Login.addInput(1, "all", (0.7*width/2), (3.5*height/5.5), 200, 50)  # password box

    #Main Menu
    Main_Menu = Menu(screen, "Main Menu", red)
    Main_Menu.addButton("Learn",200,100,red,grey,72,"Learn", (width/2),(1.5*height/5))
    Main_Menu.addButton("InfixToPost",300,100,red,grey,28,"Infix To Postfix", (width/2),(2.5*height/5))
    Main_Menu.addButton("PostToInfix",300,100,red,grey,28,"Postfix To Infix", (width/2),(3.5*height/5))
    Main_Menu.addButton("Quit",200,100,red,grey,72,"Quit",(1.75*width/2),(7*height/8.5))
    Main_Menu.addButton("Stats",200,100,red,grey,72,"Stats",(0.25*width/2),(7*height/8.5))

    #Learn menu setup
    Learn = Menu(screen, "Learn",red)
    Learn.addButton("PreOrderTree",300,100,red,grey,27,"Preorder Tree Traversal",(width/2),(1.5*height/5))
    Learn.addButton("InOrderTree",300,100,red,grey,27,"Inorder Tree Traversal",(width/2),(2.5*height/5))
    Learn.addButton("PostOrderTree",300,100,red,grey,27,"Postorder Tree Traversal",(width/2),(3.5*height/5))
    Learn.addButton("BackMM",200,100,red,grey,72,"Back",(1.75*width/2),(7*height/8.5))


    # Infix to Postfix
    InfixToPost = Menu(screen, "Infix to Postfix", red)
    InfixToPost.addButton("RandomInfix", 300, 100, red, grey, 64, "Random", (width / 2), (1.5 * height / 5))
    InfixToPost.addButton("OwnInfix", 300, 100, red, grey, 28, "Choose Your Own", (width / 2), (3 * height / 5))
    InfixToPost.addButton("BackMM", 200, 100, red, grey, 72, "Back", (1.75 * width / 2), (7 * height / 8.5))

    #Random Infix
    RandomInfix = Menu(screen, "Random Infix to Postfix", red)
    RandomInfix.addInput(0, "char", (0.7*width/2), (2*height/5), 200, 50)
    RandomInfix.addButton("BackInfix", 200, 100, red, grey, 72, "Back", (1.7*width/2), (7*height/8.5))

    #Choose your own Infix
    OwnInfix = Menu(screen, "Infix to Postfix", red)
    OwnInfix.addInput(0, "char", (0.7*width/2), (2*height/5), 200, 50)
    OwnInfix.addButton("BackInfix", 200, 100, red, grey, 72, "Back", (1.75*width/2), (7*height/8.5))

    #Postfix to Infix
    PostToInfix = Menu(screen, "Postfix to Infix", red)
    PostToInfix.addButton("RandomPost",300,100,red,grey,64,"Random",(width/2),(1.5*height/5))
    PostToInfix.addButton("OwnPost",300,100,red,grey,28,"Choose Your Own",(width/2),(3*height/5))
    PostToInfix.addButton("BackMM",200,100,red,grey,72,"Back",(1.75*width/2),(7*height/8.5))

    #Random Postfix Menu
    RandomPost = Menu(screen, "Random Postfix to Infix",red)
    RandomPost.addInput(0, "char", (0.7*width/2),(2.5*height/5), 200,50)
    RandomPost.addButton("BackPost",200,100,red,grey,72,"Back",(1.75*width/2),(7*height/8.5))


    #Choose Your own Postfix
    OwnPost = Menu(screen, "Postfix To Infix",red)
    OwnPost.addInput(0,"char",(0.7*width/2),(2.5*height/5), 200,50)
    OwnPost.addButton("BackPost",200,100,red,grey,72,"Back",(1.75*width/2),(7*height/8.5))

    #Stats page
    Stats = Menu(screen, "User Stats", red)
    Stats.addButton("BackMM",200,100,red,grey,72,"Back",(1.75*width/2),(7*height/8.5))

    #Preorder Traversal
    PreOrderInfo = Menu(screen, "Pre-Order Traversal", red)
    PreOrderInfo.addButton("PreOrderTutorial",200,100,red,grey,72,"Next",(1.75*width/2),(7*height/8.5))

    #Adding Graphical Nodes
    PreOrderTree = Menu(screen, "Pre-Order Traversal", red)
    PreOrderTree.addNode("A", width // 2, 200)  # Root node
    PreOrderTree.addNode("B", int(0.75 * width // 2), 300)  # Child node
    PreOrderTree.addNode("C", int(0.6 * width // 2), 450)  # Grandchild node
    PreOrderTree.addNode("D", int(0.9 * width // 2), 450)  # Grandchild node
    PreOrderTree.addNode("E", int(0.75 * width // 2), 550)  # Grandgrand child node
    PreOrderTree.addNode("F", int(1.25 * width // 2), 300)  # Child Node
    PreOrderTree.addNode("G", int(1.15 * width // 2), 450)  # Grandchild Node
    PreOrderTree.addNode("H", int(1.4 * width // 2), 450)  # Grandchild Node
    PreOrderTree.addButton("PreOrderContinue", 200, 100, red, grey, 54, "Continue", (1.75 * width / 2), (7 * height / 8.5))

    #Inorder Traversal
    InOrderInfo = Menu(screen, "In-Order Traversal", red)
    InOrderInfo.addButton("InOrderTutorial",200,100,red,grey,72,"Next",(1.75*width/2),(7*height/8.5))

    #Adding Graphical Nodes
    InOrderTree = Menu(screen, "In-Order Traversal", red)
    InOrderTree.addNode("A", width // 2, 200) #Root node
    InOrderTree.addNode("B",int(0.75*width//2),300) #Child node
    InOrderTree.addNode("C",int(0.6*width//2),450) #Grandchild node
    InOrderTree.addNode("D", int(0.9*width//2), 450) #Grandchild node
    InOrderTree.addNode("E", int(0.75*width//2), 550) #Grandgrand child node
    InOrderTree.addNode("F", int(1.25*width//2), 300) #Child Node
    InOrderTree.addNode("G", int(1.15*width//2), 450) #Grandchild Node
    InOrderTree.addNode("H", int(1.4*width//2), 450) #Grandchild Node
    InOrderTree.addButton("InOrderContinue", 200, 100, red, grey, 54, "Continue", (1.75 * width / 2), (7 * height / 8.5))

    #Postorder traversal
    PostOrderInfo = Menu(screen, "Post-Order Traversal", red)
    PostOrderInfo.addButton("PostOrderTutorial", 200, 100, red, grey, 72, "Next", (1.75 * width / 2), (7 * height / 8.5))

    #Adding Graphical Nodes

    PostOrderTree = Menu(screen, "Post-Order Traversal", red)
    PostOrderTree.addNode("A", width // 2, 200) #Root node
    PostOrderTree.addNode("B",int(0.75*width//2),300) #Child node
    PostOrderTree.addNode("C",int(0.6*width//2),450) #Grandchild node
    PostOrderTree.addNode("D", int(0.9*width//2), 450) #Grandchild node
    PostOrderTree.addNode("E", int(0.75*width//2), 550) #Grandgrand child node
    PostOrderTree.addNode("F", int(1.25*width//2), 300) #Child Node
    PostOrderTree.addNode("G", int(1.15*width//2), 450) #Grandchild Node
    PostOrderTree.addNode("H", int(1.4*width//2), 450) #Grandchild Node
    PostOrderTree.addButton("PostOrderContinue", 200, 100, red, grey, 54, "Continue", (1.75 * width / 2), (7 * height / 8.5))

    #Links together the visual node by simulating the creation of backend nodes, the values are chosen
    #to give a tree of the same structure as in the example. This allows the result to be calculated dynamically.
    NodeMapping = {"A":10,"B":5,"C":2,"D":4,"E":3,"F":15,"G":13,"H":17}
    NodeMappingReverse = {10:"A", 5:"B", 2:"C", 4:"D", 3:"E", 15:"F", 13:"G", 17:"H"}
    TreeRoot = Node(NodeMapping["A"])
    TreeRoot.insertNode(NodeMapping["B"])
    TreeRoot.insertNode(NodeMapping["C"])
    TreeRoot.insertNode(NodeMapping["D"])
    TreeRoot.insertNode(NodeMapping["E"])
    TreeRoot.insertNode(NodeMapping["F"])
    TreeRoot.insertNode(NodeMapping["G"])
    TreeRoot.insertNode(NodeMapping["H"])
    PreOrderResult = (TreeRoot.PreorderTraverse(TreeRoot).split(","))[:-1]
    InOrderResult = (TreeRoot.InorderTraverse(TreeRoot).split(","))[:-1]
    PostOrderResult = (TreeRoot.PostorderTraverse(TreeRoot).split(","))[:-1]
    for i in range(8):
        PreOrderResult[i] = NodeMappingReverse[int(PreOrderResult[i])]
    for i in range(8):
        InOrderResult[i] = NodeMappingReverse[int(InOrderResult[i])]
    for i in range(8):
        PostOrderResult[i] = NodeMappingReverse[int(PostOrderResult[i])]

    menu = SignUp
    def actionHandleLogin(action,menu): #defined within main due to variable scope
        if action == "SignLogin":
            menu = Login
        elif action == 'Sign Up':
            if username is not None and password is not None:
                    if sign_up(username,password):
                        menu = Login
                    return menu
        elif action == 'Login':
            if username is not None and password is not None:
                    if login(username,password):
                        menu = Main_Menu
                    return menu
        elif action == 'SignUpBack':
            menu =  SignUp
        return menu

    def actionHandleMenu(action,menu):
        if action == 'Quit':
            quit_program()
        elif action == 'Learn':
            menu = Learn
        elif action == 'PostToInfix':
            menu = PostToInfix
        elif action == 'InfixToPost':
            menu = InfixToPost
        elif action == 'Stats':
            menu = Stats
        elif action == 'BackMM': #an back button where the last menu was main menu
            menu = Main_Menu
        elif action == 'RandomPost':
            menu = RandomPost
        elif action == 'OwnPost':
            menu = OwnPost
        elif action == 'BackPost':
            menu = PostToInfix
        elif action == 'BackInfix':
            menu = InfixToPost
        elif action == 'OwnInfix':
            menu = OwnInfix
        elif action == 'RandomInfix':
            menu = RandomInfix
        elif action == 'PreOrderTree':
            menu = PreOrderInfo
        elif action == 'InOrderTree':
            menu = InOrderInfo
        elif action == 'PostOrderTree':
            menu = PostOrderInfo
        elif action == 'PreOrderTutorial':
            menu = PreOrderTree
        elif action == 'InOrderTutorial':
            menu = InOrderTree
        elif action == 'PostOrderTutorial':
            menu = PostOrderTree
        return menu


    def continueHandle(action,count):
        if action == 'PreOrderContinue' or action == 'InOrderContinue' or action == 'PostOrderContinue':
            count += 1
        return count


    #Setup loop variables
    Sign_Up_Loop = True
    Main_Menu_Loop = False
    Tree_Loop = False
    Question_Loop = False

    #Setup variables for text display
    box1_used = False
    box2_used = False
    keep_display_sign = False
    keep_display_login = False
    keep_display_random_postfix = False
    display_conversion_post = False
    correct_answer_post = False
    incorrect_answer_post = False
    correct_answer_infix = False
    incorrect_answer_infix = False
    keep_display_random_infix = False
    display_conversion_infix = False
    menu_change = True


    while Sign_Up_Loop:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            number = menu.InputClick() #Used to find out which input box is being typed into
            if event.type == pygame.QUIT:
                Sign_Up_Loop = False
                quit_program()
            elif event.type == pygame.MOUSEBUTTONDOWN and menu:
                action = menu.buttonClick(pos)
                menu = actionHandleLogin(action,menu)
            elif menu == Main_Menu: #If the main menu conditions have been met, go to the main_menu loop and record UserID
                UserID = get_userID(username)
                Sign_Up_Loop = False
                Main_Menu_Loop = True
                break
            elif event.type == pygame.KEYDOWN and menu:
                if number == 0: #First Input Box
                    box = menu.assignBox(number)
                    box.clickEvent()
                    temp = box.typeEvent(event)
                    if temp is not (True or None):
                        username = temp
                        box1_used = True
                if number == 1: #Login Password Box, only used here
                    box = menu.assignBox(number)
                    box.clickEvent()
                    temp = box.typeEvent(event)
                    if temp is not (True or None):
                        password = temp
                        box2_used = True
            menu.drawMenu()
            #Drawing persistent Text
            if menu == SignUp:
                SignUp.drawText("Username", (0.7*width/2), 190, red,32)
                SignUp.drawText("Password", (0.7*width/2), 450, red,32)
                if (box1_used and box2_used and (password or username != '')) or keep_display_sign:
                    SignUp.drawText("Sign Up unsuccessful. Error:" + " " + credentials_error(username,password), (width/5), (1.5* height / 2), red,28)
                    keep_display_sign = True
                    box1_used = False
                    box2_used = False
                    #attempts += 1 #This is used so that the text wont be removed each event cycle, when the first condition is false
            if menu == Login:
                Login.drawText("Username", (0.7*width/2), 190, red,32)
                Login.drawText("Password", (0.7*width/2), 450, red,32)
                if (box1_used and box2_used and (password or username != '')) or keep_display_login:
                    Login.drawText("Login Unsuccessful. Please check your username and password", (width/5), (1.5*height/2), red,28)
                    keep_display_login = True
                    box1_used = False
                    box2_used = False
            pygame.display.update()

    while Main_Menu_Loop:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            number = menu.InputClick()
            if event.type == pygame.QUIT:
                quit_program()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                action = menu.buttonClick(pos)
                menu = actionHandleMenu(action,menu)
            elif event.type == pygame.KEYDOWN:
                if number == 0:
                    box = menu.assignBox(number) #as there is only one box for any of the screens
                    box.clickEvent()
                    temp = box.typeEvent(event)
                    if temp is not (True or None):
                        expression = temp
                        box1_used = True
            menu.drawMenu()

            #Tree Traversal Handle

            if menu == PreOrderInfo or menu == InOrderInfo or menu == PostOrderInfo:
                #Checking to see if Tree Traversal buttons have been clicked
                Main_Menu_Loop = False
                Tree_Loop = True
                break #Break out of Main_Menu loop and go into tree loop

            #Stats Menu

            if menu == Stats:
                QuestionsAttempted = int(correct_answers(UserID)) + int(incorrect_answers(UserID))
                Stats.drawText("This user has attempted " + str(QuestionsAttempted) + " questions",(0.4*width/2),(0.7*height/2),blue,48) #How many tried
                Stats.drawText("The user has gotten " + str(correct_answers(UserID)) + " correct", (0.5*width/2),(height/2),blue,48) #How many correct

            #Postfix To Infix Conversion

            if menu == PostToInfix:
                keep_display_random_postfix = False #Used so that a new random postfix is retrieved for each time the user goes back
                correct_answer_post = False
                incorrect_answer_post = False
                QuestionNumber = get_number_questions() #Accounts for any new questions that may have been added
                count_post = 0 #A timer variable so that incorrect/correct messages only appear for a short period
            if menu == RandomPost and not keep_display_random_postfix and (pow(count_post,1,30) == 0):
                postfix = get_random_postfix(UserID,QuestionNumber) #Gives a random postfix that user has not done
                keep_display_random_postfix = True
            elif menu == RandomPost and keep_display_random_postfix:
                RandomPost.drawText(postfix, (0.65 * width / 2), 190, red, 48) #Displays question
                if box1_used or (correct_answer_post or incorrect_answer_post): #If there has been an input or the user has already inputted and got it correct or incorrect
                    QuestionID = get_QuestionID_post(postfix) #Gets questionID of postfix expression
                    if get_post_answer(postfix) == expression and not correct_answer_post:
                        update_status(QuestionID,UserID,True) #Update status in UserQuestion
                        correct_answer_post = True  #Allows correct text to display
                        box1_used = False
                    if correct_answer_post:
                            RandomPost.drawText("Correct! Well Done", (0.7 * width / 2), (3.5 * height / 5), green, 48)
                            #Displays the user got it correct
                            count_post += 1 #Counts so that after 30 events this will fade
                    if get_post_answer(postfix) != expression and not incorrect_answer_post:
                        update_status(QuestionID,UserID,False)
                        incorrect_answer_post = True
                        box1_used = False
                    if incorrect_answer_post:
                            RandomPost.drawText("Incorrect, The correct answer is " + postfix_to_infix(postfix) + "",
                                                (0.3 * width / 2), (3.5 * height / 5), red, 48)
                            count_post += 1
                    if pow(count_post,1,30) == 0:
                        #30 events have happened, correct/incorrect message must fade and new question presented
                        box1_used = False
                        correct_answer_post = False
                        incorrect_answer_post = False
                        keep_display_random_postfix = False
            elif menu == OwnPost:
                OwnPost.drawText("Enter expression to be converted and added to database",(0.5*width/2),(1.5*height/5),red,28)
                if box1_used and (check_postfix(expression)):
                    converted_postfix = postfix_to_infix(expression)
                    OwnPost.drawText("Conversion:" + converted_postfix + " ", (0.5*width/2),(4*height/5),red,48)
                    add_new_infix(converted_postfix,UserID)
                    display_conversion_post = True
                    box1_used = False
                if display_conversion_post:
                    OwnPost.drawText("Conversion:" + converted_postfix + " ", (0.5*width/2),(4*height/5),red,48)
                if box1_used:
                    OwnPost.drawText("Invalid Postfix", (0.5*width/2),(4*height/5),red,48)
                    display_conversion_post = False

            ##Infix to Postfix Conversion

            if menu == InfixToPost:
                keep_display_random_postfix = False #Used so that a new random postfix is retrieved for each time the user goes back
                correct_answer_post = False
                incorrect_answer_post = False
                count_infix = 0
                QuestionNumber = get_number_questions()
            if (menu == InfixToPost and not keep_display_random_infix) and (pow(count_infix,1,) == 0):
                infix = get_random_infix(UserID,QuestionNumber) #Gives a random postfix that user has not done
                keep_display_random_infix = True
            if menu == RandomInfix and keep_display_random_infix:
                RandomInfix.drawText(infix, (0.65 * width / 2), 190, red, 48)  # Displays question
                if box1_used or (correct_answer_infix or incorrect_answer_infix):  # If there has been an input or the user has already inputted and got it correct or incorrect
                    QuestionID = get_QuestionID_infix(infix)
                    if get_infix_answer(infix) == expression and not correct_answer_infix:
                        update_status(QuestionID, UserID, True)  # Update status in UserQuestion
                        correct_answer_infix = True
                        box1_used = False
                    if correct_answer_infix:
                        RandomInfix.drawText("Correct! Well Done", (0.7 * width / 2), (3.5 * height / 5), green, 48)
                        # Displays the user got it correct
                        count_infix += 1  # Counts so that after 30 events this will fade
                    if get_infix_answer(infix) != expression and not incorrect_answer_infix:
                        update_status(QuestionID, UserID, False)
                        incorrect_answer_infix = True
                        box1_used = False
                    if incorrect_answer_infix:
                        RandomInfix.drawText("Incorrect, The correct answer is " + infix_to_postfix(infix) + "",
                                            (0.3 * width / 2), (3.5 * height / 5), red, 48)
                        count_infix += 1
                    if pow(count_infix, 1, 30) == 0:
                        # 30 events have happened, correct/incorrect message must fade and new question presented
                        box1_used = False
                        correct_answer_infix = False
                        incorrect_answer_infix = False
                        keep_display_random_infix = False
            elif menu == OwnInfix:
                OwnInfix.drawText("Enter expression to be converted and added to database", (0.5 * width / 2),(1.5 * height / 5), red, 28)
                if box1_used and (check_infix(expression)):
                    converted_infix = infix_to_postfix(expression)
                    OwnPost.drawText("Conversion:" + converted_infix + " ", (0.5 * width / 2), (4 * height / 5), red, 48)
                    add_new_postfix(converted_infix, UserID)
                    display_conversion_infix = True
                    box1_used = False
                if display_conversion_infix:
                    OwnInfix.drawText("Conversion:" + converted_infix + " ", (0.5 * width / 2), (4 * height / 5), red, 48)
                if box1_used:
                    OwnInfix.drawText("Invalid Infix", (0.5 * width / 2), (4 * height / 5), red, 48)
                    display_conversion_infix = False

            pygame.display.update()

    #Loop handling tree traversal tutorials

    while Tree_Loop:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            action = menu.buttonClick(pos)
            if event.type == pygame.QUIT:
                quit_program()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                action = menu.buttonClick(pos)
                if menu_change:
                    menu = actionHandleMenu(action,menu)
                count = continueHandle(action, count)
            menu.drawMenu()
            if menu == PreOrderInfo:
                PreOrderInfo.drawText("Pre order traversal is used to copy a binary search tree",(0.4*width/2),(2*height/5),red,32)
                count = 0
            if menu == InOrderInfo:
                InOrderInfo.drawText("In order traversal gives the contents of a tree in ascending order",(0.4*width/2),(2*height/5),red,32)
                count = 0
            if menu == PostOrderInfo:
                PostOrderInfo.drawText("Used to convert infix notation to postfix notation aka Reverse Polish Notation (RPN)",(0.25*width/2),(2*height/5),red,32)
                PostOrderInfo.drawText("RPN is used by computers as it has no brackets making it easier to calculate and shorter to write ",(0.4*width/2),(3*height/5),red,24)
                count = 0
            if menu == PreOrderTree:
                menu_change = False
                if count == 0:
                    PreOrderTree.drawText("This is a binary search tree, press continue to traverse it",(0.5*width/2),(4*height/5),red,18)
                if count == 1:
                    PreOrderTree.visitNode(0)
                    PreOrderTree.drawText("Preorder traversal will always start at the root node, this is the only type of traversal to do this", (0.5*width/2),(4*height/5),red,18)
                if count == 2:
                    PreOrderTree.visitNode(1)
                    PreOrderTree.drawText("Following this the leftmost subtree is traversed",(0.5*width/2),(4*height/5),red,18)
                if count == 3:
                    PreOrderTree.visitNode(2)
                    PreOrderTree.drawText("C is the final node in the leftmost subtree, the algorithm goes back up one level and now goes to the right",(0.35*width/2),(4*height/5),red,18)
                if count == 4:
                    PreOrderTree.visitNode(3)
                    PreOrderTree.drawText("Now that D has been traversed, looks for the left subtree from D and finds E",(0.5*width/2),(4*height/5),red,18)
                if count == 5:
                    PreOrderTree.visitNode(4)
                    PreOrderTree.drawText("With E being traversed the entire left subtree (from A) has been traversed,the algorithm returns to the top and goes to the right",(0.1*width/2),(4*height/5),red,18)
                if count == 6:
                    PreOrderTree.visitNode(5)
                    PreOrderTree.drawText("F is the next node to be traversed, following this the algorithm goes to the left subtree of F",(0.5*width/2),(4*height/5),red,18)
                if count == 7:
                    PreOrderTree.visitNode(6)
                    PreOrderTree.drawText("From this G is traversed as it has no childrne the algorithm goes back up",(0.5*width/2),(4*height/5),red,18)
                if count == 8:
                    PreOrderTree.visitNode(7)
                    PreOrderTree.drawText("Finally H is traversed as it is the only untraversed node and the traversal is complete",(0.5*width/2),(4*height/5),red,18)
                if count == 9:
                    PreOrderTree.drawText("the result of this traversal is"+str(PreOrderResult),(0.5*width/2),(4*height/5),red,24) #result calculated earlier in code
                if count == 10: #All nodes have been traversed.
                    menu = Learn
                    menu_change = True
            if menu == InOrderTree:
                menu_change = False
                if count == 0:
                    InOrderTree.drawText("This is a binary search tree, press continue to traverse it",(0.5*width/2),(4*height/5),red,18)
                if count == 1:
                    InOrderTree.visitNode(2)
                    InOrderTree.drawText("Inorder traversal starts at the leftmost node. In this case it is C",(0.5*width/2),(4*height/5),red,18)
                if count == 2:
                    InOrderTree.visitNode(1)
                    InOrderTree.drawText("Following this the algorithm goes up and traverses B",(0.5*width/2),(4*height/5),red,18)
                if count == 3:
                    InOrderTree.visitNode(4)
                    InOrderTree.drawText("The algorithm nows goes to the highest depth possible of the right subtree (from B) meaning E is traversed",(0.35*width/2),(4*height/5),red,18)
                if count == 4:
                    InOrderTree.visitNode(3)
                    InOrderTree.drawText("The algorithm nows goes to back up and traverses D",(0.5*width/2),(4*height/5),red,18)
                if count == 5:
                    InOrderTree.visitNode(0)
                    InOrderTree.drawText("The algorithm continues to go back up until it reaches A and visits it",(0.5*width/2),(4*height/5),red,18)
                if count == 6:
                    InOrderTree.visitNode(6)
                    InOrderTree.drawText("Now the algorithm goes to the right half of the tree and goes as left and deep as possible meaning G is traversed",(0.35*width/2),(4*height/5),red,18)
                if count == 7:
                    InOrderTree.visitNode(5)
                    InOrderTree.drawText("The algorithm nows goes to back up and traverses F",(0.5*width/2),(4*height/5),red,18)
                if count == 8:
                    InOrderTree.visitNode(7)
                    InOrderTree.drawText("All other nodes have been traversed and only H is left",(0.5*width/2),(4*height/5),red,18)
                if count == 9:
                    InOrderTree.drawText("The result of the traversal is" + str(InOrderResult), (0.5*width/2),(4*height/5),red,24)
                if count == 10:
                    menu = Learn
                    menu_change = True
            if menu == PostOrderTree:
                menu_change = False
                if count == 0:
                    PostOrderTree.drawText("This is a binary search tree, press continue to traverse it",(0.5*width/2),(4*height/5),red,18)
                if count == 1:
                    PostOrderTree.drawText("Postorder traversal starts at the leftmost node. In this case it is C",(0.5*width/2),(4*height/5),red,18)
                    PostOrderTree.visitNode(2)
                if count == 2:
                    PostOrderTree.drawText("Then the algorithm goes as deep as it can on the right subtree (from B) E is traversed",(0.5*width/2),(4*height/5),red,18)
                    PostOrderTree.visitNode(4)
                if count == 3:
                    PostOrderTree.drawText("Then the algorithm goes back up one step and D is traversed",(0.5*width/2),(4*height/5),red,18)
                    PostOrderTree.visitNode(3)
                if count == 4:
                    PostOrderTree.drawText("Then the algorithm goes back up one step again and B is traversed",(0.5*width/2),(4*height/5),red,18)
                    PostOrderTree.visitNode(1)
                if count == 5:
                    PostOrderTree.drawText("Instead of visiting the root node it skips and goes straight to the right subtree where the leftmost node is traversed",(0.35*width/2),(4*height/5),red,18)
                    PostOrderTree.visitNode(6)
                if count == 6:
                    PostOrderTree.drawText("The algorithm now goes as deep as it can on the righthand side meaning H is visited",(0.5*width/2),(4*height/5),red,18)
                    PostOrderTree.visitNode(7)
                if count == 7:
                    PostOrderTree.drawText("The algorithm goes up one step and F is traversed",(0.5*width/2),(4*height/5),red,18)
                    PostOrderTree.visitNode(5)
                if count == 8:
                    PostOrderTree.drawText("With all other nodes visited the root node is visited.",(0.5*width/2),(4*height/5),red,18)
                    PostOrderTree.visitNode(0)
                if count == 9:
                    PostOrderTree.drawText("The result of the traversal is" + str(PostOrderResult), (0.5*width/2),(4*height/5),red,24)
                if count == 10:
                    menu = Learn
                    menu_change = True
            pygame.display.update()

GraphicalInterface()
#print(width//2)
#InOrderTree = Menu(screen, "In-Order Traversal", red)
#print(width // 2)
#print(0.5 * width // 2)
#print(0.25 * width // 2)
#print(0.25 * width // 2)
#print(0.1 * width // 2)
#print(1.5 * width // 2)
#print(1.25 * width // 2)
#print(1.75 * width // 2)