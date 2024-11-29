import copy
import sys
import pygame
import numpy as np
import random

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe AI")
screen.fill(BG_COLOR)

class Board:

    def __init__(self):
        self.squares = np.zeros( (ROWS, COLOUMS) )
        self.empty_sqrs = self.squares 
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            @return 0 if there is no win yet
            @return 1 if player 1 wins
            @return 2 if player 2 wins
        '''    

        for coloum in range(COLOUMS):
            if self.squares[0][coloum] == self.squares[1][coloum] == self.squares[2][coloum] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[0][coloum] == 2 else CROSS_COLOR
                    iPos = (coloum * SQUARESIZE + SQUARESIZE // 2, 20)
                    fPos = (coloum * SQUARESIZE + SQUARESIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][coloum]
            
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQUARESIZE + SQUARESIZE // 2)
                    fPos = (WIDTH - 20, row * SQUARESIZE + SQUARESIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRCLE_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        return 0
 
    def mark_sqr(self, row, coloum, player):
        self.squares[row][coloum] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, coloum):
        return self.squares[row][coloum] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for coloum in range(COLOUMS):
                if self.empty_sqr(row, coloum):
                    empty_sqrs.append( (row, coloum) )

        return empty_sqrs
    
    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0     
    

class AI:

    def __init__(self, level = 1, player = 2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] 
    
    
    def minimax(self, board, maximizing):
        
        case = board.final_state()

        if case == 1:
            return 1, None
        
        if case == 2:
            return -1, None
        
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, coloum) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, coloum, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, coloum)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, coloum) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, coloum, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, coloum)

            return min_eval, best_move

        
    def eval(self, main_board):
        if self.level == 0:

            eval = 'random'
            move = self.rnd(main_board)
        else:
            
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move 
    
class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'
        self.running  = True
        self.show_lines()

    def show_lines(self):

        screen.fill(BG_COLOR)

        pygame.draw.line(screen, LINE_COLOR, (SQUARESIZE, 0), (SQUARESIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQUARESIZE,0), (WIDTH - SQUARESIZE, HEIGHT), LINE_WIDTH)

        pygame.draw.line(screen, LINE_COLOR, (0, SQUARESIZE), (WIDTH, SQUARESIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0,HEIGHT - SQUARESIZE), (WIDTH, HEIGHT - SQUARESIZE), LINE_WIDTH)
    
    def draw_fig(self, row, coloum):
        if self.player == 1:
           
            start_desc = (coloum * SQUARESIZE + OFFSET, row * SQUARESIZE + OFFSET)
            end_desc = (coloum * SQUARESIZE + SQUARESIZE - OFFSET, row * SQUARESIZE + SQUARESIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
           
            start_asc = (coloum * SQUARESIZE + OFFSET, row * SQUARESIZE + SQUARESIZE - OFFSET)
            end_asc = (coloum * SQUARESIZE + SQUARESIZE - OFFSET, row * SQUARESIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.player == 2:
            center = (coloum * SQUARESIZE + SQUARESIZE // 2, row * SQUARESIZE + SQUARESIZE // 2)
            pygame.draw.circle(screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH) 

    def make_move(self, row, coloum):
        self.board.mark_sqr(row, coloum, self.player)
        self.draw_fig(row, coloum)
        self.next_turn()    
        
    def next_turn(self):
        self.player = self.player % 2 + 1
        
    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

        
def main():

    game = Game()
    board = game.board
    ai = game.ai

    while True:
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_g:
                    game.change_gamemode()

                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                if event.key == pygame.K_0:
                    ai.level = 0
                
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARESIZE
                coloum = pos[0] // SQUARESIZE
                
                if board.empty_sqr(row, coloum) and game.running:
                    game.make_move(row, coloum)

                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            pygame.display.update()

            row, coloum = ai.eval(board)
            game.make_move(row, coloum)

            if game.isover():
                game.running = False
            
        pygame.display.update()

main()