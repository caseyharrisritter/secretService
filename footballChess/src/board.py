from const import *
from square import Square
from piece import *
from move import Move
import random


class Board:

    def __init__(self):
        self.squareArr = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for y in range(ROWS)]
        for x in range(COLS):
            for y in range(ROWS):
                self.squareArr[x][y] = Square(x, y)
        self.eval = None
        self.gameOver = False

    def copyBoard(self):
        newBoard = Board()
        for x in range(COLS):
            for y in range(ROWS):
                newBoard.squareArr[x][y] = self.squareArr[x][y].copySquare()
        return newBoard

    def initializeBoard(self, list1, list2):
        for piece in list1:
            self.squareArr[piece.getX()][piece.getY()].setPiece(piece)

        for piece in list2:
            self.squareArr[piece.getX()][piece.getY()].setPiece(piece)

    def isLegalMove(self, move):

        def isCaptureValid(moveTuple):
            x1, y1, x2, y2 = moveTuple
            if (x1 != x2 and y1 != y2 and  # it is a diagonal move
                    self.squareArr[x2][y1].hasPiece() and
                    self.squareArr[x1][y2].hasPiece() and
                    self.squareArr[x2][y1].getPiece().getTeam() == 'off' and
                    self.squareArr[x1][y2].getPiece().getTeam() == 'off'):
                return False
            return True

        x1, y1, x2, y2 = move.tuple
        if x1 == x2 and y1 == y2:
            return True

        if x2 < 0 or x2 > COLS - 1 or y2 < 0 or y2 > ROWS - 1:
            return False

        if abs(x2 - x1) > 1 or abs(y2 - y1) > 1:
            return False

        #print("in isLegalMove", x1, y1)

        piece = self.squareArr[x1][y1].getPiece()

        if self.squareArr[x2][y2].hasPiece():  # if it is a push move
            if self.squareArr[x2][y2].getPiece().getTeam() == piece.getTeam():
                return False
            if piece.isCarrier:
                return False
            if self.squareArr[x2][y2].getPiece().isCarrier and piece.getTeam() == 'def':  # if it is a game ending capture.
                return isCaptureValid((x1, y1, x2, y2))
            x3 = (x2 - x1) + x2  # destination of pushed piece coords
            y3 = (y2 - y1) + y2

            if x3 < 0 or x3 > COLS - 1 or y3 < 0 or y3 > ROWS - 1:
                return False
            if self.squareArr[x3][y3].hasPiece():
                return False
        if piece.isCarrier and piece.getY() == 7:
            self.gameOver = True

        return True

    # return false
    #for all below cases
    # if destination is out of bounds,
    # if it is a push and the pushed piece goes out of bounds,
    # if you try to move into a space occupied by your own player (maybe set a variable to define whos turn it is based on the mover)
    # if you try to push two pieces
    # if you try to move diagonally between two servicemen in order to capture the president, so if (absVal(ax+ay) = 2 or 0),
    # and if ([startX + ax][startY] and [startX][startY + ay] are both occupied), and (dest.is president)then its false
    #try to move the same piece twice

    def applyMove(self, move):
        if move is None:
            return

        x1, y1, x2, y2 = move.tuple

        if x1 == x2 and y1 == y2:
            return

        if self.squareArr[x2][y2].hasPiece():
            if self.squareArr[x2][y2].getPiece().isCarrier:
                self.gameOver = True
                return
            x3 = (x2 - x1) + x2
            y3 = (y2 - y1) + y2
            self.applyMove(Move((x2, y2, x3, y3)))
        piece = self.squareArr[x1][y1].getPiece()

        piece.setX(x2)
        piece.setY(y2)

        self.squareArr[x1][y1].erasePiece()
        self.squareArr[x2][y2].setPiece(piece)

        if piece.isCarrier and piece.getY() == 7:
            self.gameOver = True

        #for y in range(ROWS):
         #  for x in range(COLS):
          #      if self.squareArr[x][y].hasPiece():
           #         print("0 ", end='')
            #    else:
             #       print('- ', end='')
            #print("")

    def evaluate(self):
        return random.randint(0, 10000000)


