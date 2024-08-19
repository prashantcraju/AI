import random
from random import randint
from BaseAI import BaseAI
import time
import math

class getAvailableMoves:
    infinite = float('inf')
    
    def __init__(self, grid):
        self.parent = grid
        self.blankTiles = [2, 4]
        self.depth = 0
        self.valueAlpha = -getAvailableMoves.infinite
        self.valueBeta = getAvailableMoves.infinite
        self.maxDepth = 6

    def choice(self):
        largestValue = -getAvailableMoves.infinite
        bestChoice = None
        
        for availMove in self.parent.getAvailableMoves():
            nextBox = self.parent.clone()
            nextBox.availMove(availMove)
            value = self.minimum(nextBox)
            
            if largestValue < value:
                largestValue, bestChoice = value, availMove
        return bestChoice

    def maximum(self, grid):
        self.depth += 1
        moves = grid.getAvailableMoves()
        if moves == [] or self.depth > self.maxDepth:
            self.depth -= 1
            return self.examine(grid)

        valueAlphaBeta = -getAvailableMoves.infinite

        for availMove in moves:
            nextBox = grid.clone()
            nextBox.availMove(availMove)
            valueAlphaBeta = max(valueAlphaBeta, self.minimum(nextBox))
            if valueAlphaBeta >= self.valueBeta:
                self.depth -= 1
                return valueAlphaBeta

            self.valueAlpha = max(self.valueAlpha, valueAlphaBeta)

        self.depth -= 1
        return valueAlphaBeta

    def minimum(self, grid):
        self.depth += 1
        boxes = grid.getAvailableCells()
        if boxes == [] or self.depth > self.maxDepth:
            self.depth -= 1
            return self.examine(grid)

        valueAlphaBeta = getAvailableMoves.infinite
        for box in boxes:
            for boxValue in self.blankTiles:
                nextBox = grid.clone()
                nextBox.setBoxValue(box, boxValue)
                nextValue = self.maximum(nextBox)
                valueAlphaBeta = min(valueAlphaBeta, nextValue)
                if valueAlphaBeta <= nextValue:
                    self.depth -= 1
                    return valueAlphaBeta

        self.depth -= 1
        return valueAlphaBeta

    def examine(self, grid):
        matrixSeq =    [[32768, 16384, 8192, 4096  ],
                        [  256,   512, 1024, 2048  ],
                        [  128,    64,   32,   16  ],
                        [    1,     2,    4,    8  ]]
        
        depthValue = self.depth + 1
        
        valueDiff = 0
        
        mergeValue = 0
        
        totalValue = 0
        
        seqValue = 0
        
        for r1 in range(0, 4):
            
            for r2 in range(0, 4):
                totalValue += grid.map[r1][r2]
            
                if grid.map[r1][r2] == 0:
                    pass
                seqValue += matrixSeq[r1][r2] * grid.map[r1][r2]
            
                if r1 > 0:
                    valueDiff += alphaBeta(grid.map[r1][r2] - grid.map[r1 - 1][r2])
            
                    if grid.map[r1][r2] == grid.map[r1 - 1][r2]:
                        mergeValue += grid.map[r1][r2]
            
                if r2 > 0:
                    valueDiff += alphaBeta(grid.map[r1][r2] - grid.map[r1][r2 - 1])
            
                    if grid.map[r1][r2] == grid.map[r1][r2 - 1]:
                        mergeValue += grid.map[r1][r2]
            
                if r1 < 3:
                    valueDiff += alphaBeta(grid.map[r1][r2] - grid.map[r1 + 1][r2])
            
                    if grid.map[r1][r2] == grid.map[r1 + 1][r2]:
                        mergeValue += grid.map[r1][r2]
            
                if r2 < 3:
                    valueDiff += alphaBeta(grid.map[r1][r2] - grid.map[r1][r2 + 1])
            
                    if grid.map[r1][r2] == grid.map[r1][r2 + 1]:
                        mergeValue += grid.map[r1][r2]
        
        return depthValue * (totalValue + valueDiff + mergeValue + 2 * seqValue)

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
        # Selects a random move and returns it
        moveset = grid.getAvailableMoves()
        return random.choice(moveset)[0] if moveset else None
