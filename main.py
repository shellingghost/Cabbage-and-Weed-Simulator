import pygame
import random

# CONSTANTS

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# rgb
# maybe add trail/grey post weed issue
# length of time grey each different weed
# how long each weed stays , this and above to prioritize proactive measures
# maybe dashboard with how much nutrients gets leached from the soil*
WHITE = (255, 255, 255)

EMPTY = pygame.transform.scale(pygame.image.load('download.png'), (100, 100))
CABBAGE = pygame.transform.scale(pygame.image.load('cabbage.jpg'), (100, 100))
BROWN_WEED = pygame.transform.scale(pygame.image.load('brownweed.png'), (100, 100))
ORANGE_WEED = pygame.transform.scale(pygame.image.load('orangeweed.jpg'), (100, 100))
BLUE_WEED = pygame.transform.scale(pygame.image.load('blueweed.jpg'), (100, 100))




class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.cabbage = True
        self.brown = False
        self.orange = False
        self.blue = False
        self.x = 0
        self.y = 0
        self.calc_pos()
        self.time_to_live = 0

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_orange(self):
        #self.time = random.randint(1, 3)
        self.cabbage = False
        self.orange = True
        #self.time_to_live = self.time


    def make_blue(self):
        self.time = random.randint(2, 3)
        self.cabbage = False
        self.blue = True
        self.time_to_live = self.time

    def make_brown(self):
        self.cabbage = False
        self.brown = True
        self.time_to_live = 1


    def make_cabbage(self):
        self.cabbage = True
        self.blue = False
        self.orange = False
        self.brown = False


    # change colors
    def draw(self, win):
        if self.cabbage == True:
            win.blit(EMPTY, (self.x - CABBAGE.get_width() // 2, self.y - CABBAGE.get_height() // 2))

            win.blit(CABBAGE, (self.x - CABBAGE.get_width() // 2, self.y - CABBAGE.get_height() // 2))

        if self.brown == True:
            win.blit(EMPTY, (self.x - CABBAGE.get_width() // 2, self.y - CABBAGE.get_height() // 2))

            win.blit(BROWN_WEED, (self.x - BROWN_WEED.get_width() // 2, self.y - BROWN_WEED.get_height() // 2))

        if self.orange:
            win.blit(EMPTY, (self.x - CABBAGE.get_width() // 2, self.y - CABBAGE.get_height() // 2))

            win.blit(ORANGE_WEED, (self.x - ORANGE_WEED.get_width() // 2, self.y - ORANGE_WEED.get_height() // 2))

        if self.blue:
            win.blit(EMPTY, (self.x - CABBAGE.get_width() // 2, self.y - CABBAGE.get_height() // 2))

            win.blit(BLUE_WEED, (self.x - BLUE_WEED.get_width() // 2, self.y - BLUE_WEED.get_height() // 2))

    def reset_clear(self, win):
        win.blit(EMPTY, (self.x - CABBAGE.get_width() // 2, self.y - CABBAGE.get_height() // 2))





class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    # MAY WORK AS EXPECTED!!!!!!!!!!!!!!!!!!
    # just need a white layout, maybe black lines surrounding borders
    def draw_squares(self, win):
        win.fill(WHITE)

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(Piece(row, col, WHITE))

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                piece.draw(win)


# game block
class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        # holds as key objects
        self.affected = {}

        # counters
        self.week = 0

        # keep track of objects we touch, and manually decrement them until zero with each left click
        # also keep track of how many weeks each weed occupies plots
        self.orange_ttl = 1
        self.blue_ttl = random.randint(2, 5)
        self.brown_ttl = random.randint(2, 6)

        # takes care of holding the orange positions
        self.xorange = (COLS - 1)
        self.yorange = 0

    def orange(self):
        # this function spreads the orange weed in recognizable pattern
        # start and upper right

        if self.yorange > (ROWS - 1):
            self.xorange = (COLS - 1)
            self.yorange = 0

        else:
            if self.xorange >= 0:
                # touch thee peace here
                # couldn't figure out how to use nested functions
                if random.randint(1, 3) % 2 == 0:
                    self.board.board[self.yorange][self.xorange].cabbage = False
                    self.board.board[self.yorange][self.xorange].orange = True


                # add to dictionary here
                self.affected[self.board.board[self.xorange][self.yorange]] = self.orange_ttl
                # decrement xorange
                self.xorange -= 1


            elif self.xorange < 0:
                self.yorange += 1
                self.xorange = (COLS - 1)

    def blue(self):
        # this function spreads the blue weed in a semi-recognizable pattern
        # starts lower left
        self.xblue = 0
        self.yblue = (ROWS - 1)







        direction = random.randint(1, (ROWS - 1))

        print(direction)
        self.yblue = direction
        self.xblue = direction


        # touch peace here
        print(self.xblue)
        print(self.yblue)

        self.board.board[self.yblue][self.xblue].cabbage = False
        self.board.board[self.yblue][self.xblue].blue = True

        # add to dictionary here
        self.affected[self.board.board[self.xblue][self.yblue]] = self.blue_ttl





    def brown(self):
        # this function spreads the brown weed in a random pattern
        # starts randomly
        directionvertical = random.randint(1, (ROWS - 1))
        directionhorizontal = random.randint(1, (COLS - 1))
        self.xbrown = directionvertical
        self.ybrown = directionhorizontal

        # touch peace here
        self.board.board[self.xbrown][self.ybrown].cabbage = False
        self.board.board[self.xbrown][self.ybrown].brown = True

        # add to dictionary here
        self.affected[self.board.board[self.xbrown][self.ybrown]] = self.brown_ttl


    def update(self):
        self.board.draw(self.win)
        pygame.display.update()


    def _init(self):
        self.selected = None
        self.board = Board()






FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('cabbage')







def main():
    running = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # create the weeds
                game.orange()
                game.blue()
                game.brown()

                print('increment week')
                game.week += 1

                print('iterate through the dictionary of the afflicted')
                for key, value in list(game.affected.items()):
                    print('x')
                   # print(key)
                    print(key)
                    print(value)
                    #print(value)
                    print('x')


                    game.affected[key] -= 1
                    # if it is at zero we make it a cabbage again
                    if game.affected[key] == 0:
                        key.cabbage = True
                        key.orange = False
                        key.blue = False
                        key.brown = False
                        #print(key)

                        del game.affected[key]
                        game.update()
                print(len(list(game.affected.items())))


        game.update()

    pygame.quit()


main()
