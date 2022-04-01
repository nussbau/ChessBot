import chess
import chess.engine
import random
import numpy as np
import pickle
from os import listdir


def random_board(max_depth=200):
  board = chess.Board()
  depth = random.randrange(0, max_depth)

  for _ in range(depth):
    all_moves = list(board.legal_moves)
    random_move = random.choice(all_moves)
    board.push(random_move)
    if board.is_game_over():
      break

  return board

def stockfish(board, depth):
    with chess.engine.SimpleEngine.popen_uci(r"C:\Users\nussb\Documents\Python Scripts\ChessBot\stockfish\stockfish.exe") as sf:
        result = sf.analyse(board, chess.engine.Limit(depth=depth))
        score = result['score'].white().score()
        return score

def createData(batchsize):
    boards = np.zeros((batchsize, 12, 8, 8), dtype=int)
    scores = np.zeros(batchsize)
    for x in range(batchsize):
        newBoard = random_board()
        FEN = newBoard.fen()
        SCORE = stockfish(newBoard, 0)  
        while SCORE is None:
            newBoard = random_board()
            FEN = newBoard.fen()
            SCORE = stockfish(newBoard, 0)  

        FENS = FEN.split(" ")
        
        pieces = FENS[0].split("/")
        for y in range(8):
            index = 0
            for c in pieces[y]:        
                if c == 'k':
                    boards[x][11][y][index] = -1
                elif c == 'q':
                    boards[x][10][y][index] = -1
                elif c == 'r':
                    boards[x][9][y][index] = -1
                elif c == 'b':
                    boards[x][8][y][index] = -1
                elif c == 'n':
                    boards[x][7][y][index] = -1
                elif c == 'p':
                    boards[x][6][y][index] = -1
                elif c == 'K':
                    boards[x][5][y][index] = 1
                elif c == 'Q':
                    boards[x][4][y][index] = 1
                elif c == 'R':
                    boards[x][3][y][index] = 1
                elif c == 'B':
                    boards[x][2][y][index] = 1
                elif c == 'N':
                    boards[x][1][y][index] = 1
                elif c == 'P':
                    boards[x][0][y][index] = 1
                else:
                    index += int(c)-1    
                index += 1
            
        if FENS[1] == "b":
            SCORE *= -1
        if SCORE > 15:
            SCORE = 15
        elif SCORE < -15:
            SCORE = -15    

            scores[x] = SCORE

    return boards, scores

def combineData(path, num, dataSize=1000):
    pickleNames = listdir(path)
    newPickle = open("data/chessData" + str(num), "wb")
    newXData = np.zeros((dataSize*len(pickleNames), 12, 8, 8))
    newYData = np.zeros(dataSize*len(pickleNames))
    for pickleNameIndex in range(len(pickleNames)):
        currentPickle = open(path + pickleNames[pickleNameIndex], "rb")
        xData, yData = pickle.load(currentPickle)
        for boardIndex in range(len(xData)):
            newXData[pickleNameIndex*dataSize+boardIndex] = xData[boardIndex]
            newYData[pickleNameIndex*dataSize+boardIndex] = yData[boardIndex] 
        currentPickle.close()
    pickle.dump((newXData, newYData), newPickle)
    newPickle.close()

index = 8
while index != -1:
    for x in range(29, 100):        
        print("Working on pickle number", x)
        boards, scores = createData(1000)
        file = open("chessDataPickles/chessData" + str(x) + ".pickle", "wb")
        pickle.dump((boards, scores), file)
        file.close()
    combineData("chessDataPickles/", index)
    index += 1
