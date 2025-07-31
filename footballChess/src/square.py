from piece import *


class Square:
    def __init__(self, x, y, piece=None):
        self.x = x
        self.y = y
        self.piece = piece

    def copySquare(self):
        newSquare = Square(self.x, self.y)
        if self.piece is not None:
            newSquare.setPiece(self.piece.copyPiece())
        return newSquare


    def setPiece(self, piece):
        self.piece = piece

    def getPiece(self):
        return self.piece

    def hasPiece(self):
        return self.piece is not None

    def erasePiece(self):
        self.piece = None

