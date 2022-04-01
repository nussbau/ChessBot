import pyautogui as pag
import cv2 as cv
import numpy as np
import chessBoard as cb

chessboardAccuracy = 0.02

piecePaths = [
    "greenEmpty.png",
    "whiteEmpty.png",

    "blackKingGreen.png",
    "blackKingWhite.png",
    "blackQueenGreen.png",
    "blackQueenWhite.png",
    "blackRookGreen.png",
    "blackRookWhite.png",
    "blackKnightGreen.png",
    "blackKnightWhite.png",
    "blackBishopGreen.png",
    "blackBishopWhite.png",
    "blackPawnGreen.png",
    "blackPawnWhite.png",    

    "whiteKingGreen.png",
    "whiteKingWhite.png",
    "whiteQueenGreen.png",
    "whiteQueenWhite.png",
    "whiteRookGreen.png",
    "whiteRookWhite.png",
    "whiteKnightGreen.png",
    "whiteKnightWhite.png",
    "whiteBishopGreen.png",
    "whiteBishopWhite.png",
    "whitePawnGreen.png",
    "whitePawnWhite.png"            
]

def grabChessboard():
    board = cv.imread("chessPieceImages/chessBoard.png", 0)
    final_loc = (0, 0)
    final_val = 0
    final_scale = 0

    for scaler in np.arange(0.5, 3, chessboardAccuracy):
        board = cv.resize(cv.imread("chessPieceImages//chessBoard.png", 0), (0, 0), fx=scaler, fy=scaler)
        screen = cv.cvtColor(np.array(pag.screenshot()), cv.COLOR_BGR2GRAY)
        result = cv.matchTemplate(screen, board, cv.TM_CCORR_NORMED)

        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)    
        
        if final_val < max_val:
            final_loc = max_loc
            final_val = max_val
            final_scale = scaler
        elif final_val > (max_val + 0.05):
            break
            

    if final_val > 0.97:
        board = cv.resize(cv.imread("chessPieceImages/chessBoard.png", 0), (0, 0), fx=final_scale, fy=final_scale)
        screen = screen[final_loc[1]:(final_loc[1] + board.shape[1]), final_loc[0]:(final_loc[0] + board.shape[0])]
        return screen, final_scale, final_loc
    else:
        print("Chessboard couldn't be found")
        return None, None, None



def getTile(board, x, y):
    tileWidth = round(board.shape[0]/8)
    
    return board[tileWidth*y:tileWidth*(y+1), tileWidth*x:tileWidth*(x+1)]



def createPiece(name, x, y):

    if name == "greenEmpty.png" or name == "whiteEmpty.png":
        return None
    
    Color = -1

    if name[0:5] == "white":
        Color = 0
    elif name[0:5] == "black":
        Color = 1
    
    name = name[5:]

    if name == "KingGreen.png" or name == "KingWhite.png":
        return cb.King(Color, x, y)
    elif name == "QueenGreen.png" or name == "QueenWhite.png":
        return cb.Queen(Color, x, y)
    elif name == "RookGreen.png" or name == "RookWhite.png":
        return cb.Rook(Color, x, y)
    elif name == "KnightGreen.png" or name == "KnightWhite.png":
        return cb.Knight(Color, x, y)
    elif name == "BishopGreen.png" or name == "BishopWhite.png":
        return cb.Bishop(Color, x, y)
    elif name == "PawnGreen.png" or name == "PawnWhite.png":
        return cb.Pawn(Color, x, y)
    else:
        return None



def grabPieces(chessboard, scaler):
    images = []
    pieces = []

    for path in piecePaths:
        images.append(cv.resize(cv.imread("chessPieceImages/" + path, cv.IMREAD_GRAYSCALE), (0, 0), fx=scaler, fy=scaler))

    for y in range(8):
        for x in range(8):
            tile = getTile(chessboard, x, y)

            maxIndex = 0
            maxVal = 0

            currIndex = 0
            for image in images:
                
                result = cv.matchTemplate(tile, image, cv.TM_CCORR_NORMED)

                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                
                if max_val > maxVal:
                    maxVal = max_val
                    maxIndex = currIndex

                currIndex += 1
           
            newPiece = createPiece(piecePaths[maxIndex], x, y)
            if newPiece is not None:
                pieces.append(newPiece)

    return pieces