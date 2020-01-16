import sys
import random
import copy

def is_winner(board, symbol):
    return ((board[6] == symbol and board[7] == symbol and board[8] == symbol) or # across the top
            (board[3] == symbol and board[4] == symbol and board[5] == symbol) or # across the middle
            (board[0] == symbol and board[1] == symbol and board[2] == symbol) or # across the bottom
            (board[6] == symbol and board[3] == symbol and board[0] == symbol) or # down the left side
            (board[7] == symbol and board[4] == symbol and board[1] == symbol) or # down the middle
            (board[8] == symbol and board[5] == symbol and board[2] == symbol) or # down the right side
            (board[6] == symbol and board[4] == symbol and board[2] == symbol) or # diagonal
            (board[8] == symbol and board[4] == symbol and board[0] == symbol)) # diagonal

def is_full(layout):
    for i in range(0,9):
        if(is_empty(layout,i)):
            return False
    return True

def is_empty(layout, index):
    return layout[index] == "_"

#copies board for recursion:
def copy_board(layout):
    tlayout = [0,0,0,0,0,0,0,0,0]
    for i in range(0,9):
        tlayout[i] = layout[i]
    return tlayout

#def player_move(board):
#    run = True
#    while run:
#        move = input("Please select a position to place \'X\' (0-8): ")
#        try:
#            move = int(move)
#            if (move >= 0 and move <= 8):
#                if(is_empty(board,move)):
#                    run = False
#                    board.layout[move] = 'x'
#                else:
#                    print("This space is occupied.")
#            else:
#                print("This is not a valid number.")
#        except:
#            print("Please type a number.")
#Checks to see if there is a win, loss or draw as well as calculating children and best move.

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endState = None # if this is a terminal board, endState == 'x' or 'o' for wins, or 'd' for draw, else None if this board is not final
        self.children = [] # all nodes that can be reached with a single move

        self.best_move = -1 # cell position (0-8) of the best move from this layout, or -1 if this is a final layout
        self.moves_to_end = -1 # how many moves until the end of the game, if played perfectly.  0 if this is a final layout
        self.final_state = ''  # expected final state ('x' if 'x' wins, 'o' if 'o' wins, else 'd' for a draw)

        if(is_winner(layout,'x')):
            #print("x wins and o loses.")
            self.final_state = 'x'
            self.endState = 'x'
            self.best_move = -1
            self.moves_to_end = 0
            #return 3
        elif(is_winner(layout,'o')):
            #print("o Wins and x loses.")
            self.final_state = 'o'
            self.endState = 'o'
            self.best_move = -1
            self.moves_to_end = 0
            #return 2
        elif(is_full(layout)):
            #print("draw!")
            self.final_state = 'd'
            self.endState = 'd'
            self.best_move = -1
            self.moves_to_end = 0
            #return 1
        else:
            emptyIndexes = []
            nextMove = None
            x_count = 0
            o_count = 0
            #Find ratio between the amount of x's and o's to find whose turn it is.
            for i in layout:
                if i == 'x':
                    x_count += 1
                if i == 'o':
                    o_count += 1
            if(x_count == o_count):
                nextMove = 'x'
            else:
                nextMove = 'o'

            #Fill empty array.
            for spot in range(len(layout)):
                if(is_empty(layout,spot)):
                    emptyIndexes.append(spot)
            #print("Empty Indexes: " + str(emptyIndexes))
            #Finding children.
            for idx in emptyIndexes:
                temp = copy_board(layout)
                temp[idx] = nextMove
                temp2 = BoardNode(temp)
                temp2.moveMade = idx
                self.children.append(temp2)
            #print("Board Children: " + str(board.children))
            #---------------------------
            #Best move selection.
            #---------------------------
            win = []
            draw = []
            #Separates draws and wins. (Losers aren't considered because our AI nEvEr loSeS!)
            for c in self.children:
                if(c.final_state == nextMove):
                    win.append(c)
                elif(c.final_state == 'd'):
                    draw.append(c)

            #Iterates through the winners to find out which has the least amount of moves to end.
            if(len(win) != 0):
                lowMoves = 999
                best = None
                for w in win:
                    if w.moves_to_end < lowMoves:
                        lowMoves = w.moves_to_end
                        best = w
                self.moves_to_end = best.moves_to_end + 1
                self.best_move = best.moveMade
                self.final_state = nextMove
            #Move to draw if there is no possible chance in winning.
            elif(len(draw) != 0):
                randIndex = random.randint(0,len(draw) - 1)
                self.moves_to_end = draw[randIndex].moves_to_end + 1
                self.best_move = draw[randIndex].moveMade
                self.final_state = 'd'
            #If there is no draws or wins.
            else:
                highMoves = -999
                lest = None
                for e in self.children:
                    if e.moves_to_end > highMoves:
                        highMoves = e.moves_to_end
                        lest = e
                self.moves_to_end = lest.moves_to_end + 1
                self.best_move = lest.moveMade
                if(nextMove == 'x'):
                    self.final_state = 'x'
                else:
                    self.final_state = 'o'
    def __repr__(self):
        ret_string = "\n\nTic Tac Toe Board \n"
        for i in range(0,len(self.layout)):
            if(i % 3 == 0):
                ret_string += "\n"
            ret_string += " " + self.layout[i]
        return ret_string + "\n"

if __name__ == "__main__":
    args = sys.argv
    #Create file
    write_file = open(args[1],'w')
    #Creates 9 char array of tic tac toe board and instantiates the board if arg is correct.
    board_args = list(args[2])
    #Create positions
    pos = ["top-left","top-middle","top-right","middle-left","middle-middle","middle-right","lower-left","lower-middle","lower-right"]
    if(len(board_args) == 9):
        board = BoardNode(list(args[2]))
        print(board)
    else:
        print("Board Layout is incorrect.")

    write_file.write(str(board.best_move) + "\n")
    write_file.write("Best move is ")
    write_file.write(pos[board.best_move] + "\n")
    if(board.final_state == 'd'):
        f.write("Draw in")
    else:
        write_file.write(str(board.final_state))
        write_file.write(" wins in ")
    write_file.write(str(board.moves_to_end))
    write_file.write(" moves!")
    write_file.close()
