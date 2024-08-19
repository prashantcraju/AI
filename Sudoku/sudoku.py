#!/usr/bin/env python
#coding:utf-8

"""
Name: Prashant Raju
UNI: pcr2120
HW3 Programming: sudoku.py
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

import sys
import time

ROW = "ABCDEFGHI"
COL = "123456789"

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    
    for i in ROW:
        row = ''
        
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)
        
def lowest_len(p):
    return [k for k in p.keys() if len(p.get(k))==min([len(n) for n in p.values()])]

def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    
    for r in ROW:
        
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)

def create_sudoku_board(r, c):
    brd = [box+1 for box in range(9)]
    
    for x in range(r[0],r[1]):
        
        for y in range(c[0], c[1]):
            play = board[ROW[x] + COL[y]]
            
            if play != 0:
                brd.remove(play)
    return brd
    
def spectrum(board):
    col_space = [box+1 for box in range(9)]
    row_space = [box+1 for box in range(9)]
    
    point = {ROW[r] + COL[c]: 0 for r in range(9) for c in range(9)}
    
    for p in range(9):
        
        for q in range(9):
            
            if board[ROW[p] + COL[q]] == 0:
                col_space = [box+1 for box in range(9)]
                row_space = [box+1 for box in range(9)]
                
                for x in range(9):
                    row_point = board[ROW[p] + COL[x]]
                    col_point = board[ROW[x]+ COL[q]]
                    
                    if row_point != 0:
                        row_space.remove(row_point)
                    
                    if col_point != 0:
                        col_space.remove(col_point)
                col, row = [], []
                
                if p <= 2:
                    row = [0,3]
                elif p <= 5:
                    row = [3,6]
                else:
                    row = [6,9]
                    
                if q <= 2:
                    col = [0,3]
                elif q <= 5:
                    col = [3,6]
                else:
                    col = [6,9]
                
                point[ROW[p] + COL[q]] = [index for index in [space for space in col_space if space in row_space] if index in create_sudoku_board(row, col)]
            else:
                point.pop(ROW[p]+COL[q])
    return point

def conclusion(board):
    spectr = spectrum(board)
    
    if spectr:
        spect = lowest_len(spectr)[0]
        
        if len(spectr[spect]) == 0:
            return None
        
        else:
            return True
    return True

def is_done(board):
    if True in [index == 0 for index in board.values()]:
        return False
    return True

def backtracking(board):
    """Takes a board and returns solved board."""
    # TODO: implement this
    refresh_board = spectrum(board)
    
    if is_done(board):
        return board
    tiny = lowest_len(refresh_board)[0]

    for refresh in refresh_board[tiny]:
        board[tiny] = refresh
        conclusions = conclusion(board)
        
        if conclusions is not None:
            play = backtracking(board)
            
            if play is not None:
                return play
            board[tiny] = 0
        else:
            board[tiny] = 0
    return None

if __name__ == '__main__':
    #  Read boards from source.
    src_filename = 'sudokus_start.txt'
    try:
        src_filename = sys.argv[1]
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")

    # Solve each board using backtracking
    for line in sudoku_list.split("\n"):

        if len(line) < 9:
            continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}

        # Print starting board. TODO: Comment this out when timing runs.
        print_board(board)
        
        begin = time.time()
        
        solved_board = backtracking(board)
        
        over = time.time() - begin
        
        # Solve with backtracking
        solved_board = backtracking(board)

        # Print solved board. TODO: Comment this out when timing runs.
        print_board(solved_board)
        
        print("The time it took was: ", over)

        # Write board to file
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    print("Finishing all boards in file.")
