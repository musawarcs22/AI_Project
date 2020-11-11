import arcade

# Loading needed images
background = arcade.load_texture("Images/BC.jpg") # background image
humanSnail = arcade.load_texture("Images/snail1.png") # image of human's snail
botSnail = arcade.load_texture("Images/snail2.png") # image of bots's snail
humanSplash = arcade.load_texture("Images/splash_snail1.png") # image of Human's Splash
botSplash = arcade.load_texture("Images/splash_snail2.png") # image of Bot's Splash

ROWS = 10 # number of rows in the grid
COLUMNS = 10 # number of columns in the grid

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

game_SCREEN_WIDTH = 600
game_SCREEN_HEIGHT = 600

SCREEN_TITLE = "--->SNAILS<---"

board = [] # 2D List for backEnd Matrix

G_SIZE = 60 # Size of one box

class Game(arcade.View):
    def __init__(self):
        super().__init__()

        self.initailizeBoard()
        
        #Identifiers of snails and Splashes locaions
        self.human = 1
        self.bot = 2
        self.human_Splash = 10
        self.bot_Splash = 20

        self.state = 0 # Other states can be 50(for Draw), 100(Human Win), 200(Bot win)
        self.game_state = "GameMenu" #Setting this to show menu Screen 
        self.turn = 1000 #(Human Turn) if Turn = 2000 (Bot Turn) 
        self.human_score = 0 #counter
        self.bot_score = 0 # counter

        self.human_Location = [0,0] # Initial Position of Human Snail is (0,0)
        self.Bot_Location = [9,9] # Initial Position of Bot is (9,9)
        
    
    def initailizeBoard(self):
        #The function is making the back-end 2D matrix
        #for the front end interface Grid.
        for j in range(ROWS):
            row = []
            for i in range(COLUMNS):
                row.append(0)
            board.append(row)
        board[0][0] = 1          # marker of human in the backend matrix is 1
        board[ROWS-1][COLUMNS-1] = 2 # marker of bot in the backend matrix is 2\
        for j in range(ROWS):
        	print()
        	for i in range(COLUMNS):
        		print(board[i][j], end="\t")
        print()
  
    def evaluateBoard(self):
        if self.bot_score == 50 and self.human_score == 50:
            self.game_state = "Draw"
           # return 5 # for Draw State
        elif self.bot_score > 50:
            self.game_state = "BotWon"
            #return 10 # for Bot Win
        elif self.human_score > 50:
            self.game_state = "HumanWon"
            #return 1 # for Human Win
        else:
            for i in range(10):
                for j in range(10):
                    if board[i][j] == 0:
                        self.state = 0  # Continue State
            #            return 0          game_state = "GameOn" is Continue State

    def on_key_press(self, key, modifiers):
        pass
            
    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.game_state == "GameMenu":
                self.game_state = "GameOn"
        
        elif self.game_state == "GameOn":
            box = [x//G_SIZE, y//G_SIZE]    #Location of box(x,y)
            if(self.is_Legal_Move(box)):
                self.update_grid(box)
                self.evaluateBoard()
            else:
                if self.turn == 1000:
                    self.human_score -= 1
                    self.turn = 2000

                elif self.turn == 2000:
                    self.bot_score -= 1
                    self.turn = 1000
            
    def is_Legal_Move(self,box):
        #Clicking on grid line (Not Checking and not needed)
        #Clicking on an area out of bounds(outside the GridWorld) (Checking)
        #Moving the Snail onto opponent’s Snail or Trail of Slime (Checking)
        #Playing a move by passing an empty Grid Square (Checking)
        x = box[0]
        y = box[1]
        if x <= game_SCREEN_WIDTH and y <= game_SCREEN_HEIGHT: #Checking if clicked out side screen
            
            #The following long if is checking moving on the opponent's slime
            if (self.turn == 1000 and (board[x][y] == 0 or board[x][y] == 10)) or ((self.turn == 2000) and (board[x][y] == 0 or board[x][y] == 20)): 
               
                #--------Checking Snail is not bypassing a square Start--------------#
                try: # Using these try and except blocks to ignore index error 
                    left = board[x-1][y]
                except:
                    pass
                try:
                    right = board[x+1][y]
                except:
                    pass
                try:
                    top = board[x][y+1]
                except:
                    pass
                try:
                    bottom = board[box[0]][box[1]-1]
                except:
                    pass
                if self.turn == 1000:
                    if x == 0 and y == 9:
                        if (right == 1 or bottom == 1):
                            return True
                        return False
                    elif x == 9 and y == 0:
                        if (top == 1 or left == 1):
                            return True
                        return False
                    elif x == 9 and y == 9:
                        if (bottom == 1 or left == 1):
                            return True
                        return False
                    elif x == 9 or x == 0 or y == 0 or y == 9:
                        if x == 0:
                            if (top == 1 or bottom == 1 or right == 1):
                                return True
                            return False
                        elif x == 9:
                            if (top == 1 or bottom == 1 or left == 1):
                                return True
                            return False
                        elif y == 0:
                            if (left == 1 or top == 1 or right == 1):
                                return True
                            return False
                        elif y == 9:
                            if (left == 1 or bottom == 1 or right == 1):
                                return True
                            return False
                        else:
                            return False
                    elif (x > 0 or x < 9) and (y > 0 or y < 9):
                        if (left == 1 or right == 1 or top == 1 or bottom == 1 ):
                            return True
                        return False
                
                elif self.turn == 2000:
                    if x == 0 and y == 9:
                        if  (right == 2 or bottom == 2):
                            return True
                        return False
                    elif x == 9 and y == 0:
                        if (top == 2 or left == 2):
                            return True
                        return False
                    elif x == 9 and y == 9:
                        if (bottom == 2 or left == 2):
                            return True
                        return False   
                    elif x == 9 or x == 0 or y == 0 or y == 9:
                        if x == 0:
                            if (top == 2 or bottom == 2 or right == 2 ):
                                return True
                            return False
                        elif x == 9:
                            if (top == 2 or bottom == 2 or left == 2 ):
                                return True
                            return False
                        elif y == 0:
                            if (left == 2 or top == 2 or right == 2):
                                return True
                            return False
                        elif y == 9:
                            if (left == 2 or bottom == 2 or right == 2):
                                return True
                            return False
                        else:
                            return False
                    elif (x > 0 or x < 9) and (y > 0 or y < 9):
                        if  (left == 2 or right == 2 or top == 2 or bottom == 2 ):
                            return True
                        return False
                    #--------Checking Snail is not bypassing a square End--------------#
            else:
                return False


        else:
            return False

    def update_grid(self,box):
        
        """
        This function is updating backend 2d matrix and player scores.
        box[x,y] is the location where Snail needs to be placed. 
        """

        """
       # print("\n\n\n---box = {0}".format(box))
        if self.turn == 1000:
            board[self.human_Location[0]][self.human_Location[1]] = 10
            board[box[0]][box[1]] = 1
            self.turn = 2000
            self.human_Location = box
            self.human_score += 1        #Increasing Human Score
        if self.turn == 2000:
            board[self.Bot_Location[0]][self.Bot_Location[1]] = 20
            board[box[0]][box[1]] = 2    
            self.turn = 1000
            self.Bot_Location = box     
            self.bot_score += 1         #Increasing Bot Score
        """
        #for i in range(5,0,-1):
         #   print(i)
        
        
        
        # print("\n\n\n---box = {0}".format(box))
        #Present Location of Bot 
        bx = self.Bot_Location[0] 
        by = self.Bot_Location[1]
        #Present Location of Human 
        hx = self.human_Location[0]
        hy = self.human_Location[1]
        #Desired Location where the mouse is clicked 
        cx = box[0]
        cy = box[1]
        #----------------------------------------------------
        if self.turn == 1000:     #-------> HUMAN's TURN <------------
            board[hx][hy] = 10    #Placing Splash on the Present human Location 
            self.human_score += 1 #Increasing Human Score     
            self.turn = 2000      #Changing Turn
            if board[cx][cy] == 10: #This will execute when the Human clicks on his Splash(Slippery Functionality for Human)
                if hx == cx and cy > hy:
                    for y in range(hy+1, 10, 1):
                        if y == 9 and board[cx][y]==10:
                            board[cx][y] = 1
                            self.human_Location[0] = cx
                            self.human_Location[1] = y
                            break
                        elif board[cx][y] == 0 or board[cx][y] == 20 or board[cx][y] == 2:
                            board[cx][y-1] = 1
                            self.human_Location[0] = cx
                            self.human_Location[1] = y-1
                            break
                elif hx == cx and cy < hy:
                    for y in range(hy-1, -1, -1):
                        if y == 0 and board[cx][y] == 10:
                            board[cx][y] = 1
                            self.human_Location[0] = cx
                            self.human_Location[1] = y
                            break
                        elif board[cx][y] == 0 or board[cx][y] == 20 or board[cx][y] == 2:
                            board[cx][y+1] = 1
                            self.human_Location[0] = cx
                            self.human_Location[1] = y+1
                            break
                elif cx > hx and cy == hy:
                    for x in range(cx+1, 10, 1):
                        if x == 9:
                            board[x][cy] = 1
                            self.human_Location[0] = x
                            self.human_Location[1] = cy
                            break
                        elif board[x][cy] == 0 or board[x][cy] == 20 or board[x][cy] == 2:
                            board[x-1][cy] = 1
                            self.human_Location[0] = x-1
                            self.human_Location[1] = cy
                            break
                elif cx < hx and cy == hy:
                    for x in range(cx-1, -1, -1):
                        if x == 0:
                            board[x][cy] = 1
                            self.human_Location[0] = x
                            self.human_Location[1] = cy
                            break
                        elif board[x][cy] == 0 or board[x][cy] == 20 or board[x][cy] == 2:
                            board[x+1][cy] = 1
                            self.human_Location[0] = x+1
                            self.human_Location[1] = cy
                            break
                elif cx == hx and cy == hy: #When Player will click on itself it will lose the turn and scores will remain the same
                    self.human_score -= 1 
                #----------------------------------------------------------------------------
                
            else:                   #This will execute When Human clicks Empty Square
                board[hx][hy] = 10
                board[cx][cy] = 1
                self.human_Location = box
                #----------------------------------------------------------------------------
                #----------------------------------------------------------------------------
        elif self.turn == 2000:      #-----> BOT's TURN <-----
            board[bx][by] = 20       #Putting Splash on the Bot Location
            self.turn = 1000         #Fliping turn       
            self.bot_score += 1      #Increasing Bot Score 
            if board[cx][cy] == 20:  #This will execute when the Bot clicks on his Splash(Slippery Functionality for Bot)   
                if bx == cx and cy > by:
                    for y in range(by+1, 10, 1):
                        if y == 9 and board[cx][y] == 20:
                            board[cx][y] = 2
                            self.Bot_Location[0] = cx
                            self.Bot_Location[1] = y
                            break
                        elif board[cx][y] == 0 or board[cx][y] == 10 or board[cx][y] == 1:
                            board[cx][y-1] = 2
                            self.Bot_Location[0] = cx
                            self.Bot_Location[1] = y-1
                            break
                elif bx == cx and cy <  by:
                    for y in range(by-1, -1, -1):
                        if y == 0 and board[cx][y] == 20:
                            board[cx][y] = 2
                            self.Bot_Location[0] = cx
                            self.Bot_Location[1] = y
                            break
                        elif board[cx][y] == 0 or board[cx][y] == 10 or board[cx][y] == 1:
                            board[cx][y+1] = 2
                            self.Bot_Location[0] = cx
                            self.Bot_Location[1] = y+1
                            break
                elif cx > bx and cy == by:
                    for x in range(cx+1, 10, 1):
                        if x == 9:
                            board[x][cy] = 2
                            self.Bot_Location[0] = x
                            self.Bot_Location[1] = cy
                            break
                        elif board[x][cy] == 0 or board[x][cy] == 10 or board[x][cy] == 1:
                            board[x-1][cy] = 2
                            self.Bot_Location[0] = x-1
                            self.Bot_Location[1] = cy
                            break
                elif cx < bx and cy == by:
                    for x in range(cx-1, -1, -1):
                        if x == 0:
                            board[x][cy] = 2
                            self.Bot_Location[0] = x
                            self.Bot_Location[1] = cy
                            break
                        elif board[x][cy] == 0 or board[x][cy] == 10 or board[x][cy] == 1:
                            board[x+1][cy] = 2
                            self.Bot_Location[0] = x+1
                            self.Bot_Location[1] = cy
                            break
                elif cx == bx and cy == by:
                    self.bot_score -= 1 
                #---------------------------------------------   
            else:    #This will execute When Bot clicks Empty Square
                board[bx][by] = 20
                board[cx][cy] = 2
                self.Bot_Location = box
                #---------------------------------------------

        print("-----------------------------------------------")
        for j in range(ROWS):
        	print()
        	for i in range(COLUMNS):
        		print(board[i][j], end="\t")
        print()
        
    def on_show(self):
        arcade.set_background_color(arcade.color.WOOD_BROWN) #Background color

    def on_draw(self):
        arcade.start_render()
        # self.shape_list = arcade.ShapeElementList()
        # self.shape_list.draw()

        if self.game_state == "GameMenu":
            arcade.draw_text("Menu Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Click to Start Game", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

        elif self.game_state == "GameOn":

            # setting the background image
            arcade.draw_lrwh_rectangle_textured(0, 0, game_SCREEN_WIDTH, game_SCREEN_HEIGHT, background)
            
            #Drawing Lines for playing Snail for Front End Grid.
            for x in range (0, 600, G_SIZE):
                arcade.draw_line(0, x, 600, x, arcade.color.BLACK, 4)
            for y in range (0, 600, G_SIZE):
                arcade.draw_line(y, 0, y, 600, arcade.color.BLACK, 4)

            # arcade.draw_lrwh_rectangle_textured(0, 0, game_SCREEN_WIDTH, game_SCREEN_HEIGHT, background)
            arcade.set_background_color(arcade.color.WHITE)
            arcade.draw_text("Human Score", (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)+150,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
            arcade.draw_text(str("Bot Score"), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)+50,
                        arcade.color.BLACK, font_size=15, anchor_x="center")
            arcade.draw_text(str("Turn"), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-50,
                        arcade.color.BLACK, font_size=15, anchor_x="center")

            #These for loops are maping background 2D Matrix with Front End Grid.
            for i in range(10):
                for j in range(10):
                    arcade.draw_text(str(self.human_score), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)+100,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
                    arcade.draw_text(str(self.bot_score), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2),
                         arcade.color.BLACK, font_size=15, anchor_x="center")
                    if self.turn == 1000:
                        arcade.draw_text("Human", (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-100,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
                    if self.turn == 2000:
                        arcade.draw_text("Bot", (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-100,
                         arcade.color.BLACK, font_size=15, anchor_x="center")
                    if board[i][j] == 1:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, humanSnail)
                    elif board[i][j] == 2:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, botSnail)
                    elif board[i][j] == 10:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, humanSplash)
                    elif board[i][j] == 20:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, botSplash)
        
        elif self.game_state == "Draw":
            arcade.set_background_color(arcade.color.WOOD_BROWN)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Draw", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=25, anchor_x="center")
        elif self.game_state == "HumanWon":
            arcade.set_background_color(arcade.color.WOOD_BROWN)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Human Won", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=25, anchor_x="center")
        elif self.game_state == "BotWon":
            arcade.set_background_color(arcade.color.WOOD_BROWN)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Bot Won", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=25, anchor_x="center")

def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    game_view = Game()
    window.show_view(game_view)
    arcade.run()
    
main()
