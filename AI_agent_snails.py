import arcade
import random
import copy

# Loading needed images
background = arcade.load_texture("Images/BC.jpg") # background image
humanSnail = arcade.load_texture("Images/snail1.png") # image of human's snail
botSnail = arcade.load_texture("Images/snail2.png") # image of bots's snail
humanSplash = arcade.load_texture("Images/splash_snail1.png") # image of Human's Splash
botSplash = arcade.load_texture("Images/splash_snail2.png") # image of Bot's Splash
drawEmoji = arcade.load_texture("Images/thinking.png") # image of Draw State Emoji
menuEmoji = arcade.load_texture("Images/menuBack.jpg") # image of menu_screen

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
        self.botSplash = 20

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

    def evaluateBoard_AI(self, board): # This function is changing states of the game.
        if self.bot_score == 49 and self.human_score == 49:
            self.game_state = "Draw"
            return 0
           # return 5 # for Draw State
        elif self.bot_score > 49:
            self.game_state = "BotWon"
            return 1
            #return 10 # for Bot Win
        elif self.human_score > 49:
            self.game_state = "HumanWon"
            return -1
            #return 1 # for Human Win
        else:
            for i in range(10):
                for j in range(10):
                    if board[i][j] == 0:
                        self.state = 0
                        return None  # Continue State
            #            return 0          game_state = "GameOn" is Continue State
            
            #The following conditions are necessary to tell
            # the outcome of the game if the board is completely filled.

            if self.bot_score > self.human_score:
                self.game_state = "BotWon"
                return 1
            elif self.bot_score < self.human_score:
                self.game_state = "HumanWon"
                return -1
            else:
                self.game_state = "Draw"
                return 0 
        
                        

    def evaluate(self, temp_board):  # This function is being used in recursive call of minimax ()
        h_count, b_count = 0, 0

        for i in range(10):
            for j in range(10):
                if temp_board[i][j] == 10:
                    h_count += 1
        
        for i in range(10):
            for j in range(10):
                if temp_board[i][j] == 20:
                    b_count += 1
        
        if b_count == 49 and h_count == 49:
            return 0 # for Draw State 
        elif b_count > 49:
            return 10 # for Bot Win
        elif h_count > 49:
            return -10 # for Human Win  
    def isMoveLeft(self, board):
        for i in range(ROWS):
            for j in range(COLUMNS):

                if board[i][j] == 0:
                    return True
        return False

    def childBoard(self, temp_board, turn):
        """
        This is a helper function which is called by minimax()
        and it returns the list of child boards according to
        the current location of Agent either it is Bot or Human.
        """
        temp1 = copy.deepcopy(temp_board)
        temp2 = copy.deepcopy(temp_board)
        temp3 = copy.deepcopy(temp_board)
        temp4 = copy.deepcopy(temp_board)

        childBoards = [] # This of child boards will be returned. 
        if turn:         # If turn == true, it means this is Bot's turn        
            for i in range(10):
                for j in range(10):
                    if temp_board[i][j] == self.bot:
                        x, y = j, i
                        break
            
            right, left, top, bottom = -1, -1, -1, -1

            try:
                left = temp_board[x-1][y]
            except:
                pass
            try:
                right = temp_board[x+1][y]
            except:
                pass
            try:
                top = temp_board[x][y+1]
            except:
                pass
            try:
                bottom = temp_board[x][y-1]
            except:
                pass

            # The following four if conditions are for the case
            # when there is a zero present on a possible move. 
            
            if left == 0 and x != 0: # if x==0 then it is the zeroth column and there is no left box.
                temp1[x][y] = self.botSplash
                temp1[x-1][y] = self.bot
                childBoards.append(temp1)
            
            if right == 0 and x != 9:
                temp2[x][y] = self.botSplash
                temp2[x+1][y] = self.bot
                childBoards.append(temp2)

            if top == 0 and y != 9:
                temp3[x][y] = self.botSplash
                temp3[x][y+1] = self.bot
                childBoards.append(temp3)
            
            if bottom == 0 and y != 0:
                temp4[x][y] = self.botSplash
                temp4[x][y-1] = self.bot
                childBoards.append(temp4)

            # The following four if conditions are for the case
            #  when there is bot splash present on a possible move.
             
            if left == self.botSplash:
                temp1[x][y] = self.botSplash
                for i in range(x-1, -1, -1):
                    if temp1[i][y] == 0 or temp1[i][y] == self.human or temp1[i][y] == self.human_Splash:
                        temp1[i+1][y] = self.bot
                        childBoards.append(temp1)
                        break
                    elif i == 0:
                        temp1[i][y] = self.bot
                        childBoards.append(temp1)
                        break
            
            if right == self.botSplash:
                temp2[x][y] = self.botSplash
                for i in range(x+1, 10, 1):
                    if temp2[i][y] == 0 or temp2[i][y] == self.human or temp2[i][y] == self.human_Splash:
                        temp2[i-1][y] = self.bot
                        childBoards.append(temp2)
                        break
                    elif i == 10:
                        temp2[i][y] = self.bot
                        childBoards.append(temp2)
                        break
            
            if top == self.botSplash:
                temp3[x][y] = self.botSplash
                for j in range(y+1, 10, 1):
                    if temp3[x][j] == 0 or temp3[x][j] == self.human or temp3[x][j] == self.human_Splash:
                        temp3[x][j-1] = self.bot
                        childBoards.append(temp3)
                        break
                    elif i == 10:
                        temp3[x][j] = self.bot
                        childBoards.append(temp3)
                        break
            
            if bottom == self.botSplash:
                temp4[x][y] = self.botSplash
                for j in range(y-1, -1, -1):
                    if temp4[x][j] == 0 or temp4[x][j] == self.human or temp4[x][j] == self.human_Splash:
                        temp4[x][j+1] = self.bot
                        childBoards.append(temp4)
                        break
                    elif i == 0:
                        temp4[x][j] = self.bot
                        childBoards.append(temp4)
                        break
                
            return childBoards
        
        else:# This else will execute If turn == False, means this is "Human's turn". 
            for i in range(10):
                for j in range(10):
                    if temp_board[i][j] == self.human:
                        x, y = j, i
                        break
            
            right, left, top, bottom = -1, -1, -1, -1

            try:
                left = temp_board[x-1][y]
            except:
                pass
            try:
                right = temp_board[x+1][y]
            except:
                pass
            try:
                top = temp_board[x][y+1]
            except:
                pass
            try:
                bottom = temp_board[x][y-1]
            except:
                pass

            # The following four if conditions are for the case
            # when there is a zero present on a possible move by Human. 
            
            if left == 0 and x != 0:
                temp1[x][y] = self.human_Splash
                temp1[x-1][y] = self.human
                childBoards.append(temp1)
            
            if right == 0 and x != 9:
                temp2[x][y] = self.human_Splash
                temp2[x+1][y] = self.human
                childBoards.append(temp2)

            if top == 0 and y != 9:
                temp3[x][y] = self.human_Splash
                temp3[x][y+1] = self.human
                childBoards.append(temp3)
            
            if bottom == 0 and y != 0:
                temp4[x][y] = self.human_Splash
                temp4[x][y-1] = self.human
                childBoards.append(temp4)

            # The following four if conditions are for the case
            #  when there is "Human Splash" present on a possible move.            
            
            if left == self.human_Splash:
                temp1[x][y] = self.human_Splash
                for i in range(x-1, -1, -1):
                    if temp1[i][y] == 0 or temp1[i][y] == self.bot or temp1[i][y] == self.botSplash:
                        temp1[i+1][y] = self.human
                        childBoards.append(temp1)
                        break
                    elif i == 0:
                        temp1[i][y] = self.human
                        childBoards.append(temp1)
                        break
            
            if right == self.human_Splash:
                temp2[x][y] = self.human_Splash
                for i in range(x+1, 10, 1):
                    if temp2[i][y] == 0 or temp2[i][y] == self.bot or temp2[i][y] == self.botSplash:
                        temp2[i-1][y] = self.human
                        childBoards.append(temp2)
                        break
                    elif i == 10:
                        temp2[i][y] = self.human
                        childBoards.append(temp2)
                        break
            
            if top == self.human_Splash:
                temp3[x][y] = self.human_Splash
                for j in range(y+1, 10, 1):
                    if temp3[x][j] == 0 or temp3[x][j] == self.bot or temp3[x][j] == self.botSplash:
                        temp3[x][j-1] = self.human
                        childBoards.append(temp3)
                        break
                    elif i == 10:
                        temp3[x][j] = self.human
                        childBoards.append(temp3)
                        break
            
            if bottom == self.human_Splash:
                temp4[x][y] = self.human_Splash
                for j in range(y-1, -1, -1):
                    if temp4[x][j] == 0 or temp4[x][j] == self.bot or temp4[x][j] == self.botSplash:
                        temp4[x][j+1] = self.human
                        childBoards.append(temp4)
                        break
                    elif i == 0:
                        temp4[x][j] = self.human
                        childBoards.append(temp4)
                        break
                
            return childBoards

    def minimax(self, temp_board, depth, isAgentTurn):
        """
        Our logic to make AI agent (Bot) intelligent through
        "minimax Algorithm" is that when the terminating depth
        is reached in the recursive calls of minimax() then we
        have to call “heuristic()” function on every leaf nodes
        means child boards and finds where the heuristic returns
        the maximum value and goes in that direction.
        """
        if self.evaluate(temp_board) == 10: #checking if bot won
            return self.evaluate(temp_board) - depth
        elif self.evaluate(temp_board) == -10: #checking if human won
            return self.evaluate(temp_board) + depth
        elif self.isMoveLeft(temp_board) != True: #checking game is in continue state
            return 0
        elif depth == 6: # recursive depth condition
            return self.heuristic(temp_board)

        if isAgentTurn:
            bestScore = -1000
            # bestheuristic = -1000
            if self.isMoveLeft(temp_board):
                childBoards = self.childBoard(temp_board, isAgentTurn)  #returns all child boards at current position of bot
                
                for i in childBoards:
                    score = self.minimax(i, depth+1, False)
                    # heu = self.heuristic(temp_board)
                    bestScore = max(score, bestScore)
                    # bestheuristic = max(heu, bestheuristic)
            
            return bestScore

        else:
            bestScore = 1000
            if self.isMoveLeft(temp_board):
                childBoards = self.childBoard(temp_board, isAgentTurn)  #returns all child boards at current position of human
                
                for i in childBoards:
                    score = self.minimax(i, depth+1, True)
                    bestScore = min(score, bestScore)
            
            return bestScore

    def heuristic(self, board):

        """
        Our heuristic function takes a board as input and returns
        winning chances at the current location of the Bot. We are
        calculating winning chances by applying three conditions:
        
        1) checking visited boxes by the bot and adding their count to
        winning chances.
        2) checking unvisited boxes in all four directions around the
        bot and the max of them will be added to winning chances.
        3) checking Bot’s position whether it is in the central
        area of the board or not. If it is, then winning chances
        are incremented by a value of 10. 
        """
        
        x, y, visitedBoxes, rightBoxes, leftBoxes, topBoxes, bottomBoxes, winningChances = 0, 0, 0, 0, 0, 0, 0, 0
        
        # Calculate the number of visited boxes by AI Agent and add them to the variable ‘winnigChances’.
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == self.botSplash:
                    visitedBoxes += 1
        winningChances += visitedBoxes
        
        #giving index of bot position
        for i in range(ROWS):
            for j in range(COLUMNS):
                if board[i][j] == self.bot:
                    x, y = j, i
                    break
        
        #below loops are counting zero boxes on all four sides of the bot
        for i in range(x+1, 10, 1):
            if board[i][y] == 0:
                rightBoxes += 1
            else:
                break
        for i in range(x-1, -1, -1):
            if board[i][y] == 0:
                leftBoxes += 1
            else:
                break
        for j in range(y+1, 10, 1):
            if board[x][j] == 0:
                topBoxes += 1
            else:
                break
        for j in range(y-1, -1, -1):
            if board[x][j] == 0:
                bottomBoxes += 1
            else:
                break
        
        #The number of empty boxes will be added to the variable ‘winnigChances’
        winningChances += max(rightBoxes, leftBoxes, topBoxes, bottomBoxes)
        
        # 10 will be added to the variable ‘winnigChances’ if bot is in central area.
        if((x != 0 and x != 9) and (y != 0 and y != 9)):
            winningChances += 10
        
        return winningChances

    def bot_move(self):

        """
        The Bot plays his moves using this function in such
        a way that it manually moves the Bot in all four
        directions and checks where the winning chances are
        maximum using the heuristic function. Where it gets
        the maximum winning chances, it moves the Bot in
        that direction.
        """

        #Present Location of Bot 
        bx = self.Bot_Location[0]
        by = self.Bot_Location[1]

        left_winingChance, right_winingChance, top_winingChance, bottom_winingChance = 0, 0, 0, 0
        left, right, top, bottom = -1, -1, -1, -1

        try:
            left = board[bx-1][by]
        except:
            pass
        try:
            right = board[bx+1][by]
        except:
            pass
        try:
            top = board[bx][by+1]
        except:
            pass
        try:
            bottom = board[bx][by-1]
        except:
            pass

        # moving one box in all four directions and
        # calculating heuritic values at those positions.
        
        if left == 0 and bx > 0:
            board[bx][by] = 20
            board[bx-1][by] = 2
            left_winingChance = self.heuristic(board)
            board[bx][by] = 2
            board[bx-1][by] = 0

        if right == 0 and bx < 9:#updated
            board[bx][by] = 20
            board[bx+1][by] = 2
            right_winingChance = self.heuristic(board)
            board[bx][by] = 2
            board[bx+1][by] = 0

        if top == 0 and by < 9: #updated
            board[bx][by] = 20
            board[bx][by+1] = 2
            top_winingChance = self.heuristic(board)
            board[bx][by] = 2
            board[bx][by+1] = 0

        if bottom == 0 and by > 0:
            board[bx][by] = 20
            board[bx][by-1] = 2
            bottom_winingChance = self.heuristic(board)
            board[bx][by] = 2
            board[bx][by-1] = 0

        if left != 0 and right != 0 and top != 0 and bottom != 0:
        # slippery conditions in all four directions and calculating heuritic values at that position
            if right == 20 and bx < 9:
                for i in range(bx+1, 10, 1):
                    if board[i][by] == 0 or (board[i][by] == self.human or board[i][by] == self.human_Splash):
                        if board[i][by] == 0:
                            board[bx][by] = 20
                            board[i][by] = 2
                            right_winingChance = self.heuristic(board)
                            board[bx][by] = 2
                            board[i][by] = 0
                            break
                        right_winingChance = 0
                        break

            if left == 20:
                for i in range(bx-1, -1, -1):
                    if board[i][by] == 0 or (board[i][by] == self.human or board[i][by] == self.human_Splash):
                        if board[i][by] == 0:
                            board[bx][by] = 20
                            board[i][by] = 2
                            left_winingChance = self.heuristic(board)
                            board[bx][by] = 2
                            board[i][by] = 0
                            break
                        left_winingChance = 0
                        break
            
            if top == 20:
                for j in range(by+1, 10, 1):
                    if board[bx][j] == 0 or (board[bx][j] == self.human or board[bx][j] == self.human_Splash):
                        if board[bx][j] == 0:
                            board[bx][by] = 20
                            board[bx][j] = 2
                            top_winingChance = self.heuristic(board)
                            board[bx][by] = 2
                            board[bx][j] = 0
                            break
                        top_winingChance = 0
                        break
            
            if bottom == 20:
                for j in range(by-1, -1, -1):
                    if board[bx][j] == 0 or (board[bx][j] == self.human or board[bx][j] == self.human_Splash):
                        if board[bx][j] == 0:
                            board[bx][by] = 20
                            board[bx][j] = 2
                            bottom_winingChance = self.heuristic(board)
                            board[bx][by] = 2
                            board[bx][j] = 0
                            break
                        bottom_winingChance = 0
                        break
            
            # The following 4 ifs are not working well :)
            if right == 10 or right == 1:
                right_winingChance = 0
            if left == 10 or left == 1:
                left_winingChance = 0
            if bottom == 10 or bottom == 1:
                bottom_winingChance = 0
            if top == 10 or top == 1:
                top_winingChance = 0

        # calculating where the heuristic is maximum
        if left_winingChance == max(left_winingChance, right_winingChance, top_winingChance, bottom_winingChance) and left == 0:
            board[bx][by] = 20
            board[bx-1][by] = 2
            self.Bot_Location[0] = bx-1
            self.Bot_Location[1] = by

        elif right_winingChance == max(left_winingChance, right_winingChance, top_winingChance, bottom_winingChance) and right == 0:
            board[bx][by] = 20
            board[bx+1][by] = 2
            self.Bot_Location[0] = bx+1
            self.Bot_Location[1] = by
        
        elif top_winingChance == max(left_winingChance, right_winingChance, top_winingChance, bottom_winingChance) and top == 0:
            board[bx][by] = 20
            board[bx][by+1] = 2
            self.Bot_Location[0] = bx
            self.Bot_Location[1] = by+1

        elif bottom_winingChance == max(left_winingChance, right_winingChance, top_winingChance, bottom_winingChance) and bottom == 0:
            board[bx][by] = 20
            board[bx][by-1] = 2
            self.Bot_Location[0] = bx
            self.Bot_Location[1] = by-1

        elif left_winingChance == max(left_winingChance, right_winingChance, top_winingChance, bottom_winingChance) and left == 20:
            board[bx][by] = 20
            for i in range(bx-1, -1, -1):
                    if board[i][by] == 0 or board[i][by] == self.human or board[i][by] == self.human_Splash:
                        board[i+1][by] = 2
                        self.Bot_Location[0] = i+1
                        self.Bot_Location[1] = by
                        self.bot_score -= 1
                        break
                    elif i == 0:
                        board[i][by] = 2
                        self.Bot_Location[0] = i
                        self.Bot_Location[1] = by
                        self.bot_score -= 1
                        break

        elif right_winingChance == max(left_winingChance, right_winingChance, top_winingChance, bottom_winingChance) and right == 20:
            board[bx][by] = 20
            for i in range(bx+1, 10, 1):
                    if board[i][by] == 0 or board[i][by] == self.human or board[i][by] == self.human_Splash:
                        board[i-1][by] = 2
                        self.Bot_Location[0] = i-1
                        self.Bot_Location[1] = by
                        self.bot_score -= 1
                        break
                    elif i == 9:
                        board[i][by] = 2
                        self.Bot_Location[0] = i
                        self.Bot_Location[1] = by
                        self.bot_score -= 1
                        break

        elif top_winingChance == max(left_winingChance, right_winingChance, top_winingChance, bottom_winingChance) and top == 20:
            board[bx][by] = 20
            for j in range(by+1, 10, 1):
                    if board[bx][j] == 0 or board[bx][j] == self.human or board[bx][j] == self.human_Splash:
                        board[bx][j-1] = 2
                        self.Bot_Location[0] = bx
                        self.Bot_Location[1] = j-1
                        self.bot_score -= 1
                        break
                    elif j == 9:
                        board[bx][j] = 2
                        self.Bot_Location[0] = bx
                        self.Bot_Location[1] = j
                        self.bot_score -= 1
                        break

        elif bottom_winingChance == max(left_winingChance, right_winingChance, top_winingChance, bottom_winingChance) and bottom == 20:
            board[bx][by] = 20
            for j in range(by-1, -1, -1):
                    if board[bx][j] == 0 or board[bx][j] == self.human or board[bx][j] == self.human_Splash:
                        board[bx][j+1] = 2
                        self.Bot_Location[0] = bx
                        self.Bot_Location[1] = j+1
                        self.bot_score -= 1
                        break
                    elif j == 0:
                        board[bx][j] = 2
                        self.Bot_Location[0] = bx
                        self.Bot_Location[1] = j
                        self.bot_score -= 1
                        break
            
    def on_mouse_press(self, x, y, _button, _modifiers):
        if self.game_state == "GameMenu":
                self.game_state = "GameOn"
        
        elif self.game_state == "GameOn":
            box = [x//G_SIZE, y//G_SIZE]    #Location of box(x,y)
            if(self.is_Legal_Move(box)):
                self.update_grid(box)
                self.evaluateBoard_AI(board)
                self.bot_move()
                self.update_grid(box)
                self.evaluateBoard_AI(board)
            else: #This else will execute in case the move is illegal. 
                if self.turn == 1000:
                    self.human_score -= 1
                    self.turn = 2000
                    self.bot_move()
                    self.update_grid(box)
                    self.evaluateBoard_AI(board)

                
            
    def is_Legal_Move(self,box):
        #Clicking on grid line (Not Checking and not needed)
        #Clicking on an area out of bounds(outside the GridWorld) (Checking)
        #Moving the Snail onto opponent’s Snail or Trail of Slime (Checking)
        #Playing a move by passing an empty Grid Square (Checking)
        x = box[0]
        y = box[1]
        if x <= game_SCREEN_WIDTH and y <= game_SCREEN_HEIGHT: #Checking if clicked out side screen
            
            #The following long if is checking moving on the opponent's slime
            if self.turn == 1000 and (board[x][y] == 0 or board[x][y] == 10): 
               
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
                self.human_score -= 1 #No Score should be increased if clicked on splash 
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
                    if cx == 9:              #Right Side Corner case
                        board[cx][cy] = 1
                        self.human_Location = box
                        return
                    for x in range(cx+1, 10, 1):
                        if x == 9 and board[x][cy] == 10:
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
                    if cx == 0:             #Left Side Corner case
                        board[cx][cy] = 1
                        self.human_Location = box
                        return
                    for x in range(cx-1, -1, -1):
                        if x == 0 and board[x][cy] == 10:
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
            self.bot_score += 1      #Increasing Bot Score 
            self.turn = 1000         #Fliping turn       

        print("-----------------------------------------------")
        for j in range(ROWS):
            print()
            for i in range(COLUMNS):
                print(board[i][j], end="\t")
        print()
        
    def on_show(self):
        arcade.set_background_color(arcade.color.SKY_BLUE) #Background color
        
    def on_draw(self):
        arcade.start_render()

        if self.game_state == "GameMenu":
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, menuEmoji)
            arcade.draw_text("Well Come :)", SCREEN_WIDTH-400, SCREEN_HEIGHT-100,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Start Game(Click here)", SCREEN_WIDTH-400, SCREEN_HEIGHT/2-200,
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
            arcade.set_background_color(arcade.color.WOOD_BROWN) #Background color
            arcade.draw_text("Human Score", (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)+150,
                         arcade.color.DEEP_SKY_BLUE, font_size=20, anchor_x="center")
            arcade.draw_text(str(self.human_score), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)+100,
                 arcade.color.DEEP_SKY_BLUE, font_size=15, anchor_x="center")
            arcade.draw_text(str("Bot Score"), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)+50,
                        arcade.color.DARK_RED, font_size=20, anchor_x="center")
            arcade.draw_text(str(self.bot_score), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2),
                 arcade.color.DARK_RED, font_size=15, anchor_x="center")
            
            
            if self.turn == 1000:
                
                arcade.draw_text(str("-->Turn<--"), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-50,
                        arcade.color.DEEP_SKY_BLUE, font_size=25, anchor_x="center")
                arcade.draw_text("Human", (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-100,
                 arcade.color.DEEP_SKY_BLUE, font_size=20, font_name='comic', anchor_x="center")
            
            else:
                arcade.draw_text(str("-->Turn<--"), (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-50,
                        arcade.color.DARK_RED, font_size=25, anchor_x="center")
                arcade.draw_text("Bot", (game_SCREEN_WIDTH/2)+400, (game_SCREEN_HEIGHT/2)-100,
                 arcade.color.DARK_RED, font_size=20, font_name='comic', anchor_x="center")
            
            #These for loops are maping background 2D Matrix with Front End Grid.
            for i in range(10):
                
                for j in range(10):
                    
                    if board[i][j] == 1:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, humanSnail)
                    
                    elif board[i][j] == 2:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, botSnail)
                    
                    elif board[i][j] == 10:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, humanSplash)
                    
                    elif board[i][j] == 20:
                        arcade.draw_lrwh_rectangle_textured(G_SIZE*i+5, G_SIZE*j, G_SIZE-10, G_SIZE-10, botSplash)
        
        elif self.game_state == "Draw":

            arcade.set_background_color(arcade.color.BISQUE)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("It's a Draw :(", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=30, bold=True, anchor_x="center")
            arcade.draw_lrwh_rectangle_textured(325, 400, 200, 200, drawEmoji)
        
        elif self.game_state == "HumanWon":
            
            arcade.set_background_color(arcade.color.DEEP_SKY_BLUE)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Human Won", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=30, anchor_x="center")
            arcade.draw_lrwh_rectangle_textured(325, 400, 200, 200, humanSnail)
        
        elif self.game_state == "BotWon":
            
            arcade.set_background_color(arcade.color.LIGHT_PINK)
            arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center") # These for writing text on screen
            arcade.draw_text("Bot Won", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=30, anchor_x="center")
            arcade.draw_lrwh_rectangle_textured(325, 400, 200, 200, botSnail)             

def main():

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
    game_view = Game()
    window.show_view(game_view)
    arcade.run()
    
main()
