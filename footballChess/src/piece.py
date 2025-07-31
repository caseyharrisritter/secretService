import os


class Piece:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isCarrier = False
        self.moved = False
        self.texture = None
        self.texture_rect = None
        self.team = None

    def copyPiece(self):
        newPiece = Piece(self.x, self.y)
        newPiece.isCarrier = self.isCarrier
        newPiece.moved = self.moved
        newPiece.team = self.team

        return newPiece



    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self,x):
        self.x = x

    def setY(self,y):
        self.y = y

    def getTexture(self):
        return self.texture
    def getTeam(self):
        return self.team


class Off(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.team = 'off'
        size = 80
        self.texture = os.path.join(f'assets/images/imgs-{size}px/white_pawn.png')


class Carrier(Off):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.isCarrier = True
        size = 80
        print('in carrier init')
        self.texture = os.path.join(f'assets/images/imgs-{size}px/white_king.png')


class Def(Piece):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.team = 'def'

        size = 80
        self.texture = os.path.join(f'assets/images/imgs-{size}px/black_pawn.png')

