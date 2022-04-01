import numpy as np
import pickle
import torch
import neuralNetwork as nn

PATH = "chessEngine.model"

if torch.cuda.is_available():  
  dev = "cuda:0" 
else:  
  dev = "cpu"  
device = torch.device(dev)  

try:
    checkpoint = torch.load(PATH)
except:
    checkpoint = None
    
#Building the network
learningRate = 3e-4
batchSize = 128
numEpochs = 50
testSize = 0.05
seed = 8008153

#network = nn.neuralNet()
network = nn.convNet()

if checkpoint is not None:
    network.load_state_dict(checkpoint['model_state_dict'])

def forward(network, X):
    activations = []
    input = X

    for layer in network:
        activations.append(layer.forward(input))
        input = activations[-1]

    assert len(activations) == len(network)
    return activations[-1]

def getNewBoard(board, move):
    newBoard = board.copy()
    
    newX, newY = move[1]
    oldY, oldX = move[0].Location
    
    newBoard[newY][newX] = newBoard[oldX][oldY]
    newBoard[oldX][oldY] = 0

    return (newBoard, move)

def findBestBoard(boards):
    if len(boards) == 0:
        return None

    bestBoard = boards[0]

    for x in range(1, len(boards)):
        bestBoard = compareBoardState(bestBoard, boards[x])

    return bestBoard   

def convertBoardState(board):
    boardArray = np.zeros((12, 8, 8))
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[x][y] == 0:
                continue
            if board[x][y] == 1:
                boardArray[0][y][x] = 1
            elif board[x][y] == -1:
                boardArray[1][y][x] = -1
            elif board[x][y] == 2:
                boardArray[2][y][x] = 1
            elif board[x][y] == -2:
                boardArray[3][y][x] = -1
            elif board[x][y] == 3:
                boardArray[4][y][x] = 1
            elif board[x][y] == -3:
                boardArray[5][y][x] = -1
            elif board[x][y] == 5:
                boardArray[6][y][x] = 1
            elif board[x][y] == -5:
                boardArray[7][y][x] = -1
            elif board[x][y] == 9:
                boardArray[8][y][x] = 1
            elif board[x][y] == -9:
                boardArray[9][y][x] = -1
            elif board[x][y] == 50:
                boardArray[10][y][x] = 1
            elif board[x][y] == -50:
                boardArray[11][y][x] = -1
    return boardArray.flatten()


#This is how we rate board states
def compareBoardState(boardState1, boardState2):
    b1 = network(torch.tensor(convertBoardState(boardState1[0])).float().view(-1, 12, 8, 8))
    b2 = network(torch.tensor(convertBoardState(boardState2[0])).float().view(-1, 12, 8, 8))
    
    if b1 > b2:
        return boardState1
    elif b2 > b1:
        return boardState2