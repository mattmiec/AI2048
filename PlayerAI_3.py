import random
import sys
import time
from BaseAI_3 import BaseAI

timelimit = 0.2
# set weighting for heuristic function
alpha = 0.25
beta = 0.25
gamma = 0.25

class PlayerAI(BaseAI):
    def getMove(self, grid):
        # Selects a random move and returns it
        startTime = time.process_time()
        #moveset = grid.getAvailableMoves()
        #move = random.choice(moveset)[0] if moveset else None

        maxdepth = 5
        #while time.process_time() - startTime < timelimit:
        #    # iterative deepening
        #    maxdepth += 1
        move = None
        newBestMove = minimaxDecision(grid, maxdepth)
        if newBestMove != None:
            # newBestMove will be None if miniMaxDecision timed out
            move = newBestMove

        if move is not None:
            return move[0]
        else:
            return None


def minimaxDecision(grid, maxdepth):
    # get best move for given grid and max depth with minimax algorithm
    # return none if timed out

    #print()
    max_move = None
    max_util = 0
    alpha = grid.getMaxTile()
    beta = sys.maxsize
    for move in grid.getAvailableMoves():
        util = minValue(move[1], maxdepth, alpha, beta)
        #print("maxdepth = ", maxdepth)
        #print("minvalue = ", util)
        if util > max_util:
            max_move = move
            max_util = util
    #print("final max_util = ", max_util)
    #print("decision = ", max_move[0])
    return max_move


def maxValue(grid, maxdepth, alpha, beta):
    # cutoff test
    if maxdepth == 0:
        #print("eval = ", eval(grid))
        return eval(grid)
    moves = grid.getAvailableMoves()
    max_util = grid.getMaxTile()
    # terminal test
    if len(moves) == 0:
        return eval(grid)
    for move in moves:
        util = minValue(move[1], maxdepth - 1, alpha, beta)
        #print("maxdepth = ", maxdepth)
        #print("minvalue = ", util)
        max_util = max(util, max_util)
        if max_util >= beta:
            return max_util
        alpha = max(alpha, util)
    return max_util


def minValue(grid, maxdepth, alpha, beta):
    # cutoff test
    if maxdepth == 0:
        #print("eval = ", eval(grid))
        return eval(grid)
    cells = grid.getAvailableCells()
    # terminal test
    if len(cells) == 0:
        return eval(grid)
    else:
        min_util = grid.getMaxTile()
        for cell in cells:
            for val in (2,4):
                newgrid = grid.clone()
                newgrid.insertTile(cell, val)
                util = maxValue(newgrid, maxdepth - 1, alpha, beta)
                #print("maxdepth = ", maxdepth)
                #print("maxvalue = ", util)
                min_util = min(util, min_util)
                if min_util <= alpha:
                    return min_util
                beta = min(beta, util)
        return min_util


def eval(grid):
    # each component is normalized to 1
    nec = number_empty_cells(grid)/16
    nav = number_adjacent_values(grid)/24
    mic = int(is_max_in_corner(grid))
    print("nec = {}, nav = {}, mic = {}".format(nec, nav, mic))
    return alpha*nec + beta*nav + gamma*mic

def number_empty_cells(grid):
    result = len(grid.getAvailableCells())
    #print("number of empty cells = ", result)
    return result

def number_adjacent_values(grid):
    result = 0
    for i in range(4):
        for j in range(4):
            if grid.crossBound((i+1, j)):
                if grid.getCellValue((i+1, j)) == grid.getCellValue((i, j)) and grid.getCellValue((i,j)) is not None:
                    result += 1
            if grid.crossBound((i, j+1)):
                if grid.getCellValue((i, j+1)) == grid.getCellValue((i, j)) and grid.getCellValue((i,j)) is not None:
                    result += 1
    #print("num of adjacent values = ", result)
    return result


def is_max_in_corner(grid):
    maxval = grid.getMaxTile()
    if grid.getCellValue((0, 0)) == maxval:
        #print("Max tile is in corner: ", True)
        return True
    if grid.getCellValue((3, 0)) == maxval:
        #print("Max tile is in corner: ", True)
        return True
    if grid.getCellValue((0, 3)) == maxval:
        #print("Max tile is in corner: ", True)
        return True
    if grid.getCellValue((3, 3)) == maxval:
        #print("Max tile is in corner: ", True)
        return True
    #print("Max tile is in corner: ", False)
    return False
