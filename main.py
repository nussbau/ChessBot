import pyautogui as pag
import time
import boardSelection as bs
import chessBoard as cb
import setup

def makeMove(board, boardLocation, move):
    oldX, oldY = move[0].Location
    newX, newY = move[1]

    boardTileWidth = board.shape[0]/8
    
    oldX = (boardTileWidth * oldX) + (boardTileWidth/2) + boardLocation[0]
    oldY = (boardTileWidth * oldY) + (boardTileWidth/2) + boardLocation[1]
    newX = (boardTileWidth * newX) + (boardTileWidth/2) + boardLocation[0]
    newY = (boardTileWidth * newY) + (boardTileWidth/2) + boardLocation[1]

    pag.moveTo(oldX, oldY)
    pag.mouseDown()
    pag.moveTo(newX, newY, .5, pag.easeOutQuad)
    pag.mouseUp()

cont = True

Board = cb.chessBoard()
Color = None

time.sleep(3)

while cont:
    ts = time.time()
    print("Time start")

    chessboard, scaler, boardLoc = setup.grabChessboard()
    if chessboard is None:
        continue
    print("Chessboard found: " + str(time.time()-ts))
    
    Pieces = setup.grabPieces(chessboard, scaler) 
    Board.setPieces(Pieces)

    print("Pieces found: " + str(time.time()-ts))

    if Color is None:
        Color = Board.Board[7][7].Color        

    moves = Board.getMoves(Pieces, Color)
    
    newBoard = Board.returnBoard(Color)

    possibleBoards = []

    #We're gonna have to change this (returns the board for each move)
    for pieceMove in moves:
        possibleBoards.append(bs.getNewBoard(newBoard, pieceMove))

    #Finds the board in possibleBoards with the highest score
    bestBoard = bs.findBestBoard(possibleBoards)
    #Makes the move (duh)
    makeMove(chessboard, boardLoc, bestBoard[1])

    print("Time stop: " + str(time.time()-ts))
    time.sleep(1.5)
    #cont = False