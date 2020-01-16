import sys
import random
import copy

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endState = None # if this is a terminal board, endState == 'x' or 'o' for wins, or 'd' for draw, else None if this board is not final
        self.children = [] # all nodes that can be reached with a single move

        self.best_move = -1 # cell position (0-8) of the best move from this layout, or -1 if this is a final layout
        self.moves_to_end = -1 # how many moves until the end of the game, if played perfectly.  0 if this is a final layout
        self.final_state = ''  # expected final state ('x' if 'x' wins, 'o' if 'o' wins, else 'd' for a draw)
    def __repr__(self):
        ret_string = "\n\nTic Tac Toe Board \n"
        for i in range(0,len(self.layout)):
            if(i % 3 == 0):
                ret_string += "\n"
            ret_string += " " + self.layout[i]
        return ret_string + "\n"

def player_move(board):
    run = True
    while run:
        move = input("Please select a position to place \'X\' (0-8): ")
        try:
            move = int(move)
            if (move >= 0 and move <= 8):
                if(is_empty(board,move)):
                    run = False
                    board.layout[move] = 'x'
                else:
                    print("This space is occupied.")
            else:
                print("This is not a valid number.")
        except:
            print("Please type a number.")

def is_winner(board, symbol):
    return ((board.layout[6] == symbol and board.layout[7] == symbol and board.layout[8] == symbol) or # across the top
            (board.layout[3] == symbol and board.layout[4] == symbol and board.layout[5] == symbol) or # across the middle
            (board.layout[0] == symbol and board.layout[1] == symbol and board.layout[2] == symbol) or # across the bottom
            (board.layout[6] == symbol and board.layout[3] == symbol and board.layout[0] == symbol) or # down the left side
            (board.layout[7] == symbol and board.layout[4] == symbol and board.layout[1] == symbol) or # down the middle
            (board.layout[8] == symbol and board.layout[5] == symbol and board.layout[2] == symbol) or # down the right side
            (board.layout[6] == symbol and board.layout[4] == symbol and board.layout[2] == symbol) or # diagonal
            (board.layout[8] == symbol and board.layout[4] == symbol and board.layout[0] == symbol)) # diagonal

def is_full(board):
    for i in range(0,9):
        if(is_empty(board,i)):
            return False
    return True

def is_empty(board, index):
    return board.layout[index] == "_"

#Checks to see if there is a win, loss or draw.
def check_wld(board):
    if(is_winner(board,'x')):
        print("x wins and o loses.")
        board.final_state = 'x'
        return 3
    elif(is_winner(board,'o')):
        print("o Wins and x loses.")
        board.final_state = 'o'
        return 2
    elif(is_full(board)):
        print("draw!")
        board.final_state = 'd'
        return 1
    else:
        emptyIndexes = []
        nextMove = None
        x_count = 0
        o_count = 0
        #Find ratio between the amount of x's and o's to find whose turn it is.
        for i in board.layout:
            if i == 'x':
                x_count += 1
            if i == 'o':
                o_count += 1
        if(x_count == o_count):
            nextMove = 'x'
        else:
            nextMove = 'o'

        #Fill empty array.
        for spot in range(len(board.layout)):
            if(is_empty(board,spot)):
                emptyIndexes.append(spot)
        print("Empty Indexes: " + str(emptyIndexes))
        #Finding children.
        for idx in emptyIndexes:
            temp = copy_board(board)
            temp.layout[idx] = nextMove
            temp.moveMade = idx
            board.children.append(temp)
        print("Board Children: " + str(board.children))


#copies board for recursion:
def copy_board(board):
    layout =[0,0,0,0,0,0,0,0,0]
    for i in range(0,9):
        layout[i] = board.layout[i]
    return BoardNode(layout)

#Gets best move/computer AI
def best_move(board, symbol):
    if(is_winner(board,'x')):
        print("x wins and o loses.")
        board.final_state = 'x'
        return 3
    elif(is_winner(board,'o')):
        print("o Wins and x loses.")
        board.final_state = 'o'
        return 2
    elif(is_full(board)):
        print("draw!")
        board.final_state = 'd'
        return 1

if __name__ == "__main__":
    args = sys.argv
    #Create file
    write_file = open(args[1],'w')
    #Creates 9 char array of tic tac toe board and instantiates the board if arg is correct.
    board_args = list(args[2])
    if(len(board_args) == 9):
        board = BoardNode(list(args[2]))
        print(board)
    else:
        print("Board Layout is incorrect.")

    check_wld(board)
