import sys
import time
from BaseAI_3 import BaseAI

timelimit = 0.2
# set weighting for heuristic function
alpha = 0.3 # weighting for empty-spaces
beta = 0.3 # weighting for adjacent and matching tiles
delta = 0.2 # weighting for putting the max tile in top-left corner
gamma = 0.2 # weighting for left to right, up to down monotonic ordering

class PlayerAI(BaseAI):

    def getMove(self, grid):
        self.starttime = time.process_time()
        print()
        maxdepth = 1
        move = None
        while time.process_time() - self.starttime < timelimit:
            # iterative deepening
            newBestMove = self.minimaxDecision(grid, maxdepth)
            if newBestMove is not None:
                # newBestMove will be None if miniMaxDecision timed out
                move = newBestMove
                print("maxdepth = {}".format(maxdepth))
            maxdepth += 2
        if move is not None:
            return move[0]
        else:
            return None

    def minimaxDecision(self, grid, maxdepth):
        # get best move for given grid and max depth with expectiminimax algorithm
        # return none if timed out
        max_move = None
        max_util = 0
        alpha = 0
        beta = 1
        for move in grid.getAvailableMoves():
            if time.process_time() - self.starttime > timelimit:
                return None
            util = self.minValue(move[1], maxdepth-1, alpha, beta)
            if util is None:
                return None
            if util > max_util:
                max_move = move
                max_util = util
        return max_move

    def maxValue(self, grid, maxdepth, alpha, beta):
        # cutoff test
        if maxdepth == 0:
            return eval(grid)
        moves = grid.getAvailableMoves()
        max_util = 0
        # terminal test
        if len(moves) == 0:
            return eval(grid)
        for move in moves:
            if time.process_time() - self.starttime > timelimit:
                return None
            util = self.minValue(move[1], maxdepth - 1, alpha, beta)
            if util is None:
                return None
            max_util = max(util, max_util)
            if max_util >= beta:
                return max_util
            alpha = max(alpha, util)
        return max_util

    def minValue(self, grid, maxdepth, alpha, beta):
        # cutoff test
        if maxdepth == 0:
            return eval(grid)
        cells = grid.getAvailableCells()
        # terminal test
        if len(cells) == 0:
            return eval(grid)
        else:
            # minvalue given that new tile is a 2
            min_util = 1
            for cell in cells:
                if time.process_time() - self.starttime > timelimit:
                    return None
                newgrid = grid.clone()
                newgrid.insertTile(cell, 2)
                util = self.maxValue(newgrid, maxdepth - 1, alpha, beta)
                if util is None:
                    return None
                min_util = min(util, min_util)
                if min_util <= alpha:
                    return min_util
                beta = min(beta, util)
            min_util_2 = min_util

            # minvalue given that new tile is a 4
            min_util = 1
            for cell in cells:
                if time.process_time() - self.starttime > timelimit:
                    return None
                newgrid = grid.clone()
                newgrid.insertTile(cell, 4)
                util = self.maxValue(newgrid, maxdepth - 1, alpha, beta)
                if util is None:
                    return None
                min_util = min(util, min_util)
                if min_util <= alpha:
                    return min_util
                beta = min(beta, util)
            min_util_4 = min_util

            # return expectation minvalue
            return .9 * min_util_2 + .1 * min_util_4


def eval(grid):
    # each component is normalized to 1
    nec = number_empty_cells(grid)/16
    nav = number_adjacent_values(grid)/24
    mic = is_max_in_corner(grid)
    mon = monotonicity(grid)
    return alpha*nec + beta*nav + delta*mic + gamma*mon


def number_empty_cells(grid):
    result = len(grid.getAvailableCells())
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
    return result


def is_max_in_corner(grid):
    # check whether max tile is in top left corner
    if grid.getCellValue((0, 0)) == grid.getMaxTile():
        return 1
    return 0


def monotonicity(grid):
    # check for non-increasing ordering from left to right and top to bottom
    score = 0
    for i in range(4):
        lastval = grid.getCellValue((i, 0))
        if lastval != 0:
            score += 1
            for j in range(1, 4):
                val = grid.getCellValue((i,j))
                if (val == 0) or (val > lastval):
                    break
                else:
                    lastval = val
                    score += 1
    for j in range(4):
        lastval = grid.getCellValue((0, j))
        if lastval != 0:
            score += 1
            for i in range(1, 4):
                val = grid.getCellValue((i, j))
                if (val == 0) or (val > lastval):
                    break
                else:
                    lastval = val
                    score += 1

    # normalize to number of tiles on board
    numTiles = 16 - len(grid.getAvailableCells())

    # and normalize to 1
    return float(score)/float(2. * numTiles)
