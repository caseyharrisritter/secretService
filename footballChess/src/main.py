import sys

import pygame
from game import Game
from const import *
from dragger import Dragger
from move import Move
import time


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('footballChess')
        self.game = Game()

    def mainloop(self):
        screen = self.screen
        game = self.game
        dragger = game.dragger
        board = self.game.board
        cpuDelay = 0
        cpuMoveIt = 0
        cpuMoving = False


        while not board.gameOver:
            game.show_bg(screen)
            game.showPieces(screen)
            if dragger.dragging:
                dragger.update_blit(screen)

            if cpuMoving:
                if cpuDelay % 600 == 0:
                    board.applyMove(game.offMoveList[cpuMoveIt])
                    game.show_bg(screen)
                    game.showPieces(screen)
                    cpuMoveIt += 1
                cpuDelay += 1

                if cpuMoveIt > 4:
                    cpuMoveIt = 0
                    cpuMoving = False
                    cpuDelay = 0
                    game.updateGame(True)




            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        board = game.tempBoard
                        game.offPieceList = game.getOffPieceList(board)
                        game.defPieceList = game.getDefPieceList(board)
                        print('in key pressed 2')

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 3 and game.cpu and game.noPiecesMoved() and game.turn == 'off':

                        for move in game.getCPUMove2(False):
                            board.applyMove(move)
                            game.show_bg(screen)
                            game.showPieces(screen)
                            pygame.display.flip()  # <— show this step
                            pygame.time.delay(1500)  # pause so we can see it
                        # final state already on screen; can skip extra flip if you like
                        game.updateGame(True)
                        continue


                        # for move in game.getCPUMove2(False): # incomplete search, no backwards moves
                        #     board.applyMove(move)
                        #     game.show_bg(screen)
                        #     game.showPieces(screen)
                        # game.show_bg(screen)
                        # game.showPieces(screen)
                        #     #time.sleep(1)
                        # game.updateGame(True)
                        # continue



                    if event.button == 2 and game.noPiecesMoved() and game.turn == 'off':
                        for move in game.getCPUMove2(True):  # full search, backwards moves included
                            board.applyMove(move)
                            game.show_bg(screen)
                            game.showPieces(screen)
                            pygame.display.flip()  # <— show this step
                            pygame.time.delay(1500)  # pause so we can see it
                            # final state already on screen; can skip extra flip if you like
                        game.updateGame(True)
                        continue



                    dragger.update_mouse(event.pos)
                    clickedX = dragger.mouseX // SQSIZE
                    clickedY = dragger.mouseY // SQSIZE

                    if board.squareArr[clickedX][clickedY].hasPiece():
                        piece = board.squareArr[clickedX][clickedY].getPiece()
                        if not piece.moved and piece.getTeam() == game.turn:
                            dragger.drag_piece(piece)
                            game.show_bg(screen)
                            game.showPieces(screen)

                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        game.show_bg(screen)
                        game.showPieces(screen)
                        dragger.update_blit(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        releasedY = dragger.mouseY // SQSIZE
                        releasedX = dragger.mouseX // SQSIZE

                        move = Move((dragger.piece.getX(), dragger.piece.getY(), releasedX, releasedY))

                        if board.isLegalMove(move):
                            board.applyMove(move)
                            dragger.piece.moved = True
                            game.updateGame()


                        dragger.undrag_piece()
                    game.show_bg(screen)
                    game.showPieces(screen)

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            pygame.display.update()



def playComputerMove(board, game, screen, moveList):
    i = 0
    while(i < 2500):

        if i % 500 == 0:
            move = moveList[i // 500]
            board.applyMove(move)

        game.show_bg(screen)
        game.showPieces(screen)
        pygame.display.update()
    game.updateGame(True)


main = Main()

main.mainloop()
