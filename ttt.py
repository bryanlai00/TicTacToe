import sys

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
        return ret_string


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
