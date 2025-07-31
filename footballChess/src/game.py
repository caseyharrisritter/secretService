from board import Board
from piece import *
from const import *
from dragger import Dragger
from move import Move
from turn import Turn
import random
import pygame
import math
from itertools import permutations
import queue


class Game:
    def __init__(self):
        self.board = Board()
        self.offPieceList = [Carrier(5, 1), Off(3, 2), Off(4, 2), Off(5, 2), Off(6, 2)]
        self.defPieceList = [Def(3, 5), Def(4, 5), Def(5, 5), Def(6, 5)]
        self.board.initializeBoard(self.offPieceList, self.defPieceList)
        self.dragger = Dragger()
        self.offMoveList = []  # list of 5 moves
        self.defMoveList = []  # list of 4 moves,
        self.turn = 'def'
        self.cpu = True
        self.tempBoard = self.board.copyBoard()
        # to make this better, Game should probably have 2 Player attributes, and the Player object has a list of pieces, the turn is also just a Player

    def show_bg(self, surface):
        for x in range(COLS):
            for y in range(ROWS):
                if (x + y) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)

                rect = (x * SQSIZE, y * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def showPieces(self, surface):

        for list in (self.offPieceList, self.defPieceList):
            for piece in list:
                if piece is not self.dragger.piece:

                    img = pygame.image.load(piece.getTexture())
                    img_center = piece.getX() * SQSIZE + SQSIZE // 2, piece.getY() * SQSIZE + SQSIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)

    def switchTurn(self):
        self.turn = 'def' if self.turn == 'off' else 'off'

    def updateGame(self, afterCPU=False):

        if afterCPU:
            self.turn = 'def'
            for piece in self.offPieceList:
                piece.moved = False
            self.tempBoard = self.board.copyBoard()
            return

        if self.turn == 'def':
            for piece in self.defPieceList:
                if not piece.moved:
                    return
            self.switchTurn()
            for piece in self.defPieceList:
                piece.moved = False
            self.tempBoard = self.board.copyBoard()
            return
        if self.turn == 'off':
            for piece in self.offPieceList:
                if not piece.moved:
                    return
            self.switchTurn()
            for piece in self.offPieceList:
                piece.moved = False
            self.tempBoard = self.board.copyBoard()
            return

    def noPiecesMoved(self):
        for piece in self.defPieceList:
            if piece.moved:
                return False
        for piece in self.offPieceList:
            if piece.moved:
                return False

        return True

    def getCPUMoves(self, fullSearch):  # 12 minutes for 2021385 legal moves out of 7,000,000,000 possible
        print("THINKING... DON'T TOUCH... beholding 20,000 moves per second...")
        bestMoveList = None
        bestEval = self.evaluate(self.board)

        if fullSearch:
            yLowerLimit = -1
        else:
            yLowerLimit = 0

        i = 0
        for first in self.offPieceList:
            for second in self.offPieceList:
                if second is first:
                    continue
                for third in self.offPieceList:
                    if third is second or third is first:
                        continue
                    for fourth in self.offPieceList:
                        if fourth is first or fourth is second or fourth is third:
                            continue
                        for fifth in self.offPieceList:
                            if fifth is first or fifth is second or fifth is third or fifth is fourth:
                                continue
                            #itOfList = [first, second, third, fourth, fifth]

                            for xadj1 in range(-1, 2):
                                for yadj1 in range(yLowerLimit, 2):

                                    for xadj2 in range(-1, 2):
                                        for yadj2 in range(yLowerLimit, 2):

                                            for xadj3 in range(-1, 2):
                                                for yadj3 in range(yLowerLimit, 2):

                                                    for xadj4 in range(-1, 2):
                                                        for yadj4 in range(yLowerLimit, 2):

                                                            for xadj5 in range(-1, 2):
                                                                for yadj5 in range(yLowerLimit, 2):
                                                                    #print(i)
                                                                    #i = i + 1

                                                                    moveList = [
                                                                        Move((first.x, first.y, first.x + xadj1,
                                                                              first.y + yadj1)),
                                                                        Move((second.x, second.y, second.x + xadj2,
                                                                              second.y + yadj2)),
                                                                        Move((third.x, third.y, third.x + xadj3,
                                                                              third.y + yadj3)),
                                                                        Move((fourth.x, fourth.y, fourth.x + xadj4,
                                                                              fourth.y + yadj4)),
                                                                        Move((fifth.x, fifth.y, fifth.x + xadj5,
                                                                              fifth.y + yadj5))
                                                                    ]

                                                                    # moveList = [
                                                                    #     Move((p[0].x, p[0].y, p[0].x + xadj1,
                                                                    #           p[0].y + yadj1)),
                                                                    #     Move((p[1].x, p[1].y, p[1].x + xadj2,
                                                                    #           p[1].y + yadj2)),
                                                                    #     Move((p[2].x, p[2].y, p[2].x + xadj3,
                                                                    #           p[2].y + yadj3)),
                                                                    #     Move((p[3].x, p[3].y, p[3].x + xadj4,
                                                                    #           p[3].y + yadj4)),
                                                                    #     Move((p[4].x, p[4].y, p[4].x + xadj5,
                                                                    #           p[4].y + yadj5))
                                                                    # ]

                                                                    tempBoard = self.board.copyBoard()
                                                                    illegal = False
                                                                    for move in moveList:
                                                                        if tempBoard.isLegalMove(move):
                                                                            tempBoard.applyMove(move)
                                                                        else:
                                                                            illegal = True
                                                                            break

                                                                    if illegal:
                                                                        continue

                                                                    i = i + 1
                                                                    eval = self.evaluate(tempBoard)
                                                                    if eval > bestEval:
                                                                        bestEval = eval
                                                                        bestMoveList = moveList
                                                                        #if i>5000:
                                                                        #print('returned')
                                                                        #return bestMoveList

                                                                        #if i>10000:
                                                                        #   for move in bestMoveList:
                                                                        #      print(move.x1, move.y1, move.x2, move.y2)
                                                                        #     self.board.applyMove(move)
                                                                        #return
        for move in bestMoveList:
            print(move.x1, move.y1, '-', move.x2, move.y2)
        print(i, "legal moves out of 7,000,000")
        return bestMoveList

        print(bestEval)
        for move in bestMoveList:
            #print(move.x1,move.y1,move.x2,move.y2)
            self.board.applyMove(move)
            self.show_bg(screen)
            self.showPieces(screen)

    def getCPUMove2(self, fullSearch):  # 5 minutes for 2,021,385 legal moves out of 7,000,000
        print("THINKING... DON'T TOUCH... evaluating 20,000 moves per second...")
        bestMoves = []
        bestEval = self.evaluate(self.board)
        turnList = [Turn(bestEval, None, None), Turn(bestEval, None, None), Turn(bestEval, None, None),
                    Turn(bestEval, None, None), Turn(bestEval, None, None)]

        if fullSearch:
            yLowerLimit = -1
        else:
            yLowerLimit = 0

        i = 0
        for first in self.offPieceList:
            for second in self.offPieceList:
                if second is first:
                    continue
                for third in self.offPieceList:
                    if third is second or third is first:
                        continue
                    for fourth in self.offPieceList:
                        if fourth is first or fourth is second or fourth is third:
                            continue
                        for fifth in self.offPieceList:
                            if fifth is first or fifth is second or fifth is third or fifth is fourth:
                                continue
                            #itOfList = [first, second, third, fourth, fifth]

                            tempBoard = self.board.copyBoard()

                            for xadj1 in range(-1, 2):
                                for yadj1 in range(yLowerLimit, 2):
                                    move1 = Move((first.x, first.y, first.x + xadj1,
                                                  first.y + yadj1))
                                    tempBoard1 = tempBoard.copyBoard()
                                    #print(first.x, first.y, first.x + xadj1,
                                    #first.y + yadj1)
                                    if tempBoard1.isLegalMove(move1):
                                        tempBoard1.applyMove(move1)
                                    else:
                                        continue

                                    for xadj2 in range(-1, 2):
                                        for yadj2 in range(yLowerLimit, 2):
                                            move2 = Move((second.x, second.y, second.x + xadj2,
                                                          second.y + yadj2))
                                            tempBoard2 = tempBoard1.copyBoard()

                                            if tempBoard2.isLegalMove(move2):
                                                tempBoard2.applyMove(move2)
                                            else:
                                                continue

                                            for xadj3 in range(-1, 2):
                                                for yadj3 in range(yLowerLimit, 2):
                                                    move3 = Move((third.x, third.y, third.x + xadj3,
                                                                  third.y + yadj3))
                                                    tempBoard3 = tempBoard2.copyBoard()
                                                    if tempBoard3.isLegalMove(move3):
                                                        tempBoard3.applyMove(move3)
                                                    else:
                                                        continue

                                                    for xadj4 in range(-1, 2):
                                                        for yadj4 in range(yLowerLimit, 2):
                                                            move4 = Move((fourth.x, fourth.y, fourth.x + xadj4,
                                                                          fourth.y + yadj4))
                                                            tempBoard4 = tempBoard3.copyBoard()
                                                            if tempBoard4.isLegalMove(move4):
                                                                tempBoard4.applyMove(move4)
                                                            else:
                                                                continue

                                                            for xadj5 in range(-1, 2):
                                                                for yadj5 in range(yLowerLimit, 2):
                                                                    move5 = Move((fifth.x, fifth.y, fifth.x + xadj5,
                                                                                  fifth.y + yadj5))
                                                                    tempBoard5 = tempBoard4.copyBoard()
                                                                    if tempBoard5.isLegalMove(move5):
                                                                        tempBoard5.applyMove(move5)
                                                                    else:
                                                                        continue

                                                                    eval = self.evaluate(tempBoard5)

                                                                    # if eval > bestEval:
                                                                    #     bestEval = eval
                                                                    #     bestMoves = [move1,move2,move3,move4,move5]

                                                                    if eval > turnList[0].eval:
                                                                        turnList[0] = Turn(eval,
                                                                                           [move1, move2, move3, move4,
                                                                                            move5], tempBoard5)
                                                                        turnList.sort(key=lambda x: x.eval)

        return turnList[4].moveList

        for move in bestMove:
            print(move.x1, move.y1, '-', move.x2, move.y2)
        print(i, "legal moves out of 7,000,000")
        return bestMoves

    def getDefMove(self):
        pass

    def evaluate(self, board):
        #print("arrived evaluate function")
        #return random.randint(0,100000)

        pieceList = []
        totalPoints = 0
        for x in range(COLS):
            for y in range(ROWS):
                if board.squareArr[x][y].hasPiece():
                    pieceList.append(board.squareArr[x][y].getPiece())

        for piece in pieceList:
            if piece.isCarrier:
                kingx = piece.x
                kingy = piece.y

        totalPoints = 250 * kingy

        defDistance = 0
        offDistance = 0
        det = 0
        pos = 0
        for piece in pieceList:
            if piece.team == 'def':
                dist = math.sqrt((piece.x - kingx) ** 2 + (piece.y - kingy) ** 2)
                defDistance = defDistance + dist
                if dist < 2:
                    det = det + 2000
                    if board.squareArr[kingx][piece.y].hasPiece() and board.squareArr[piece.x][kingy].hasPiece():
                        if board.squareArr[kingx][piece.y].getPiece().getTeam() == 'off' and board.squareArr[piece.x][
                            kingy].getPiece().getTeam() == 'off':
                            det = det - 1975
            else:
                dist = math.sqrt((piece.x - kingx) ** 2 + (piece.y - kingy) ** 2)
                offDistance = offDistance + dist
                if dist < 2 and (piece.y == kingy + 1):
                    pos = pos + 25
                if piece.y == kingy - 1:
                    det = det + 15

        totalPoints = totalPoints + (20 * defDistance) - (100 * offDistance) - det + pos

        if kingy == 7:
            return 99999999

        if False:
            print(totalPoints)
            for y in range(ROWS):
                for x in range(COLS):
                    if board.squareArr[x][y].hasPiece():
                        print("0 ", end='')
                    else:
                        print('- ', end='')
            print("")

        return totalPoints

    def getOffPieceList(self, board):
        listy = []
        for x in range(COLS):
            for y in range(ROWS):
                if board.squareArr[x][y].hasPiece():
                    piece = board.squareArr[x][y].getPiece()
                    if piece.getTeam() == 'off':
                        listy.append(piece)
        return listy

    def getDefPieceList(self, board):
        listy = []
        for x in range(COLS):
            for y in range(ROWS):
                if board.squareArr[x][y].hasPiece():
                    piece = board.squareArr[x][y].getPiece()
                    if piece.getTeam() == 'def':
                        listy.append(piece)
        return listy
