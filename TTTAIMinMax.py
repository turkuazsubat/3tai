import copy
import sys
import pygame
import random
import numpy as np

from TTTcons import *
#__SETUP
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic Tac Toe with AI(Min-Max Algorithm)")
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))
        self.empty_sqrs = self.squares # [squares]
        self.marked_sqrs = 0


    def win(self,p=0):
        if p == 1 or p==0:
            m1= pygame.font.SysFont("FUTURA",30)
            m2= pygame.font.SysFont("FUTURA",25)
                
            t1 = m1.render("AI is Win",1,CIRC_COLOR )
            t2 = m2.render("AI always wins because AI is a product of mind,",1,WIN_LINE_COLOR )
            t3 = m2.render("and humans are helpless in the face of superior reason",1,WIN_LINE_COLOR )
            screen.blit(t1,(850,250))
            screen.blit(t2,(700,280))
            screen.blit(t3,(680,310))
            pygame.display.update()


    def mark_sqr(self,row,col,player):
        self.squares[row][col] = player
        self.marked_sqrs += 1
    
    def empty_sqr(self,row,col):
        return self.squares[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        
        return empty_sqrs
    
   
    
    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0
    
    def final_state(self,show=False):
        '''
        @return = 0, if there no win yet
        @return = 1, if player 1 wins
        @return = 2, if player 2 wins
        '''

        #vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] !=0:
                if show:
                    color = WIN_LINE_COLOR if self.squares[0][col] ==2 else WIN_LINE_COLOR
                    iPos = (col * SQSIZE +SQSIZE // 2,20)
                    fPos = (col * SQSIZE + SQSIZE//2,HEIGHT-20)
                    pygame.draw.line(screen, color, iPos,fPos,CROSS_WIDTH)

                return self.squares[0][col]

        #horizontal wins    
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] !=0:
                if show:                   
                    color = WIN_LINE_COLOR if self.squares[row][0] ==2 else WIN_LINE_COLOR
                    iPos = (20,row*SQSIZE+SQSIZE//2)
                    fPos = (GAME_WIDHT-20,row*SQSIZE+SQSIZE//2)
                    pygame.draw.line(screen, color, iPos,fPos,CROSS_WIDTH)
                    
                    
                    
                return self.squares[row][0]
            
        #desc diagonal wins
            if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] !=0:
                if show:
                    
                    color = WIN_LINE_COLOR if self.squares[1][1] ==2 else WIN_LINE_COLOR
                    iPos = (20,20)
                    fPos = (GAME_WIDHT-20,HEIGHT-20)
                    pygame.draw.line(screen, color, iPos,fPos,CROSS_WIDTH)
                    
                    
                return self.squares[1][1]
            
        #asc diagonal wins
            if self.squares[0][2] == self.squares[1][1] == self.squares[2][0] !=0:
                if show:
                    
                    color = WIN_LINE_COLOR if self.squares[1][1] ==2 else WIN_LINE_COLOR
                    iPos = (20,HEIGHT-20)
                    fPos = (GAME_WIDHT-20,20)
                    pygame.draw.line(screen, color, iPos,fPos,CROSS_WIDTH)
                    
                return self.squares[1][1]

        #no win yet
        return 0  

class AI:

    def __init__(self,level=1,player=2):
        self.level = level
        self.player = player
        
    Mess = ""

    def rnd(self,board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0,len(empty_sqrs))
        

        return empty_sqrs[idx] #(row,col)
    
    def minimax(self,board,maximazing):
        
        #terminal case
        case = board.final_state()

        #player 1 wins

        if case == 1:
            return 1,None #Eval, movee

        #player 2 wins
        
        if case == 2:
            return -1,None

        #draw

        if board.isfull():
            return 0,None
        
        #-----

        if maximazing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for(row,col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval = self.minimax(temp_board,False)[0] ##WHATTTA
                if eval > max_eval: ###
                    max_eval = eval
                    best_move = (row,col)
            return max_eval, best_move

        elif not maximazing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for(row,col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval = self.minimax(temp_board,True)[0] ##WHATTTA
                if eval < min_eval: ###
                    min_eval = eval
                    best_move = (row,col)
            return min_eval, best_move
                


        

    def eval(self,main_board):
        if self.level == 0:
            #random choice
            eval = 'random'
            move = self.rnd(main_board)
            
        else:
            #minimax algorithm choice
            eval , move = self.minimax(main_board,False)
            
        
        #ai min max outputs
        #print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')

        return move #row,col


class Game:

    def __init__(self):
        self.board=Board()
        self.ai = AI()
        self.player=1 #1-Cross 2-circles
        self.gamemode = 'ai' # pvp or ai
        self.running  = True
        self.show_lines()
        
    

    def make_move(self,row,col):
        
            self.board.mark_sqr(row,col,self.player)
            self.draw_fig(row,col)
            self.next_turn()
            self.whoplay()

    
          
    def show_lines(self):
        #For Reset Re-Painting the table
        screen.fill(BG_COLOR)
        #vertical
        #notes:first parameter is start xy coordinat and secont parameter is x-y end coordinat
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HEIGHT),LINE_WIDHT)
        pygame.draw.line(screen,LINE_COLOR,(2*SQSIZE,0),(2*SQSIZE,HEIGHT),LINE_WIDHT)
        pygame.draw.line(screen,LINE_COLOR,(GAME_WIDHT,0),(GAME_WIDHT,HEIGHT),LINE_WIDHT//2)
        #horizontal
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(GAME_WIDHT,SQSIZE),LINE_WIDHT)
        pygame.draw.line(screen,LINE_COLOR,(0,2*SQSIZE),(GAME_WIDHT,HEIGHT-SQSIZE),LINE_WIDHT)
        #Player Line
        pygame.draw.line(screen,LINE_COLOR,(650,125),(1150,125),150)
        pygame.draw.line(screen,LINE_COLOR,(650,300),(1150,300),150)
        pygame.draw.line(screen,LINE_COLOR,(675,425),(875,425),50)
        pygame.draw.line(screen,LINE_COLOR,(925,425),(1125,425),50)
            #__fonts
        m= pygame.font.SysFont("FUTURA",30)
            #Btn Restart Config
        BR = m.render("Reset",1,WIN_LINE_COLOR)
        screen.blit(BR,(750,415))
            #Btn GameMode
        BG = m.render("Game Mode",1,WIN_LINE_COLOR  )
        screen.blit(BG,(965,415))
        pygame.display.update()
        
    def whoplay(self,s=False):

        pygame.draw.line(screen,LINE_COLOR,(650,125),(1150,125),150)
        m= pygame.font.SysFont("FUTURA",30)
        text= f'Player Number {self.player}, is played'  
        BR = m.render(text,1,WIN_LINE_COLOR)
        screen.blit(BR,(775,125))
        if s ==True:
            print("d")
        
        pygame.display.update()
    
    def next_turn(self):
        self.player = self.player % 2 + 1

    def draw_fig(self,row,col):
        if self.player == 1:
            #draw cross
            #--desc line
            start_desc = (col * SQSIZE + OFFSET,row * SQSIZE +OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET,row * SQSIZE + SQSIZE-OFFSET)
            #--asc line
            start_asc = (col * SQSIZE + OFFSET,row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET,row * SQSIZE + OFFSET)

            pygame.draw.line(screen,CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)
            pygame.draw.line(screen,CROSS_COLOR,start_asc,end_asc,CROSS_WIDTH)

        elif self.player == 2:
            #draw circles
            center = (col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2)
            pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRC_WIDTH)

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == "pvp" else "pvp"
        print(f'game mode is {self.gamemode}')
        
        ''' if self.gamemode == "pvp":self.gamemode = "ai"
            else: self.gamemode = "pvp" '''

    def reset(self):
        self.__init__()

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()
    

def main():
    #object
    game = Game()
    board=game.board
    ai = game.ai
    
    

    #mainloop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                pos = event.pos
                if pos[0] <= 600 and pos[1] <= 600:
                    row=pos[1]//SQSIZE #Y
                    col=pos[0]//SQSIZE #X
                    
                
                    if board.empty_sqr(row,col) and game.running:
                        game.make_move(row,col)
                        #print(board.squares)

                        if game.isover():                          
                            game.running  = False 
                            
                            
                        
                                        
                
                else:
                    #print(pos[0],pos[1])
                    if (pos[0] >= 675 and pos[0] <=875) and (pos[1] >=400 and pos[1] <=450):
                        game.reset()
                        board = game.board
                        ai=game.ai
                    
                    if (pos[0] >= 925 and pos[0] <=1125) and (pos[1] >=400 and pos[1] <=450):
                        game.change_gamemode()





            if event.type == pygame.KEYDOWN:
                
                #g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                '''
                #r- restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai=game.ai
                '''
                #0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0   
                #1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1
                        



        if game.gamemode == "ai" and game.player == ai.player and game.running:
            #update the screen
            pygame.display.update()

            #ai methods
            row,col = ai.eval(board)
            game.make_move(row,col)

            if game.isover():
                
                board.win(game.player)
                game.running  = False

        pygame.display.update()

main()