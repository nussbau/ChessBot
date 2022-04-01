import numpy as np



class chessBoard:

    def __init__(self) -> None:
        self.Board = [[None for y in range(8)] for x in range(8)]

    def setPieces(self, Pieces):
        for y in range(8):
            for x in range(8):
                self.Board[x][y] = None
        for piece in Pieces:
            x, y = piece.Location
            self.Board[x][y] = piece

    def printBoard(self):
        for y in range(8):
            for x in range(8):
                if self.Board[x][y] is not None:
                    print(self.Board[x][y].toString(), end=" ")
                else:
                    print("Empty", end=" ")
            
            print("")

    def getMoves(self, Pieces, Color):
        possibleMoves = []
        for piece in Pieces:
            if piece.Color == Color:
                pieceMoves = piece.returnMoves(self.Board)
                if pieceMoves is not None:
                    for move in pieceMoves:
                        possibleMoves.append((piece, move))
        return possibleMoves
            

    def returnBoard(self, Color):
        board = np.zeros((8, 8), dtype=int)
        for y in range(8):
            for x in range(8):
                if self.Board[x][y] is not None:
                    if isinstance(self.Board[x][y], Pawn):
                        if self.Board[x][y].Color == Color:
                            board[x][y] = 1
                        else:
                            board[x][y] = -1
                    elif isinstance(self.Board[x][y], Knight):
                        if self.Board[x][y].Color == Color:
                            board[x][y] = 2
                        else:
                            board[x][y] = -2
                    if isinstance(self.Board[x][y], Bishop):
                        if self.Board[x][y].Color == Color:
                            board[x][y] = 3
                        else:
                            board[x][y] = -3
                    if isinstance(self.Board[x][y], Rook):
                        if self.Board[x][y].Color == Color:
                            board[x][y] = 5
                        else:
                            board[x][y] = -5
                    if isinstance(self.Board[x][y], Queen):
                        if self.Board[x][y].Color == Color:
                            board[x][y] = 9
                        else:
                            board[x][y] = -9
                    if isinstance(self.Board[x][y], King):
                        if self.Board[x][y].Color == Color:
                            board[x][y] = 50
                        else:
                            board[x][y] = -50

        return board.T

class chessPiece:
    
    def __init__(self, Color, x, y) -> None:
        self.Color = Color
        self.Location = (x, y)

    def setLocation(self, x, y):
        self.Location = (x, y)

    def returnMoves(self, board):
        return None

    def toString(self):
        return "Empty"
        


class Queen(chessPiece):

    def __init__(self, Color, x, y):
        super().__init__(Color, x, y)

    def returnMoves(self, board):
        possibleMoves = []
        x, y = self.Location

        for newX in range(x-1, -1, -1):
            if board[newX][y] is not None:
                if board[newX][y].Color != self.Color:
                    possibleMoves.append((newX, y))                
                break
            possibleMoves.append((newX, y))

        for newX in range(x+1, 8):
            if board[newX][y] is not None:
                if board[newX][y].Color != self.Color:
                    possibleMoves.append((newX, y))                
                break
            possibleMoves.append((newX, y))

        for newY in range(y-1, -1, -1):
            if board[x][newY] is not None:
                if board[x][newY].Color != self.Color:
                    possibleMoves.append((x, newY))                
                break
            possibleMoves.append((x, newY))
        
        for newY in range(y+1, 8):
            if board[x][newY] is not None:
                if board[x][newY].Color != self.Color:
                    possibleMoves.append((x, newY))                
                break
            possibleMoves.append((x, newY))



        newX = x-1
        newY = y-1
        while newX >= 0 and newY >= 0:
            if board[newX][newY] is not None:
                if board[newX][newY].Color != self.Color:
                    possibleMoves.append((newX, newY))                
                break
            possibleMoves.append((newX, newY))
            newX -= 1
            newY -= 1
        
        newX = x+1
        newY = y-1
        while newX < 8 and newY >= 0:
            if board[newX][newY] is not None:
                if board[newX][newY].Color != self.Color:
                    possibleMoves.append((newX, newY))                
                break
            possibleMoves.append((newX, newY))
            newX += 1
            newY -= 1

        newX = x+1
        newY = y+1
        while newX < 8 and newY < 8:
            if board[newX][newY] is not None:
                if board[newX][newY].Color != self.Color:
                    possibleMoves.append((newX, newY))                
                break
            possibleMoves.append((newX, newY))
            newX += 1
            newY += 1

        newX = x-1
        newY = y+1
        while newX >= 0 and newY < 8:
            if board[newX][newY] is not None:
                if board[newX][newY].Color != self.Color:
                    possibleMoves.append((newX, newY))                
                break
            possibleMoves.append((newX, newY))
            newX -= 1
            newY += 1


        return possibleMoves

    def toString(self):
        if self.Color == 0:
            return "White Queen"
        else:
            return "Black Queen"



class Rook(chessPiece):

    def __init__(self, Color, x, y):
        super().__init__(Color, x, y)

    def returnMoves(self, board):
        possibleMoves = []
        x, y = self.Location

        for newX in range(x-1, -1, -1):
            if board[newX][y] is not None:
                if board[newX][y].Color != self.Color:
                    possibleMoves.append((newX, y))                
                break
            possibleMoves.append((newX, y))

        for newX in range(x+1, 8):
            if board[newX][y] is not None:
                if board[newX][y].Color != self.Color:
                    possibleMoves.append((newX, y))                
                break
            possibleMoves.append((newX, y))

        for newY in range(y-1, -1, -1):
            if board[x][newY] is not None:
                if board[x][newY].Color != self.Color:
                    possibleMoves.append((x, newY))                
                break
            possibleMoves.append((x, newY))
        
        for newY in range(y+1, 8):
            if board[x][newY] is not None:
                if board[x][newY].Color != self.Color:
                    possibleMoves.append((x, newY))                
                break
            possibleMoves.append((x, newY))
        
        return possibleMoves

    def toString(self):
        if self.Color == 0:
            return "White Rook"
        else:
            return "Black Rook"



class Knight(chessPiece):

    def __init__(self, Color, x, y):
        super().__init__(Color, x, y)

    def returnMoves(self, board):
        possibleMoves = []
        x, y = self.Location
        knightMoves = [(x+1, y+2), (x-1, y+2), (x+1, y-2), (x-1, y-2),
                         (x+2, y+1), (x-2, y+1), (x+2, y-1), (x-2, y-1)]

        for move in knightMoves:
            newX, newY = move
            if newX < 8 and newX >= 0:
                if newY < 8 and newY >= 0:
                    if board[newX][newY] is None or board[newX][newY].Color != self.Color:
                        possibleMoves.append(move)
        return possibleMoves

    def toString(self):
            if self.Color == 0:
                return "White Knight"
            else:
                return "Black Knight"



class Bishop(chessPiece):

    def __init__(self, Color, x, y):
        super().__init__(Color, x, y)

    def returnMoves(self, board):
        possibleMoves = []
        x, y = self.Location

        newX = x-1
        newY = y-1
        while newX >= 0 and newY >= 0:
            if board[newX][newY] is not None:
                if board[newX][newY].Color != self.Color:
                    possibleMoves.append((newX, newY))                
                break
            possibleMoves.append((newX, newY))
            newX -= 1
            newY -= 1
        
        newX = x+1
        newY = y-1
        while newX < 8 and newY >= 0:
            if board[newX][newY] is not None:
                if board[newX][newY].Color != self.Color:
                    possibleMoves.append((newX, newY))                
                break
            possibleMoves.append((newX, newY))
            newX += 1
            newY -= 1

        newX = x+1
        newY = y+1
        while newX < 8 and newY < 8:
            if board[newX][newY] is not None:
                if board[newX][newY].Color != self.Color:
                    possibleMoves.append((newX, newY))                
                break
            possibleMoves.append((newX, newY))
            newX += 1
            newY += 1

        newX = x-1
        newY = y+1
        while newX >= 0 and newY < 8:
            if board[newX][newY] is not None:
                if board[newX][newY].Color != self.Color:
                    possibleMoves.append((newX, newY))                
                break
            possibleMoves.append((newX, newY))
            newX -= 1
            newY += 1


        return possibleMoves

    def toString(self):
        if self.Color == 0:
            return "White Bishop"
        else:
            return "Black Bishop"



class Pawn(chessPiece):

    def __init__(self, Color, x, y):
        super().__init__(Color, x, y)

    def returnMoves(self, board):
        possibleMoves = []
        x, y = self.Location
        #Moves
        if board[x][y-1] is None:
            if y == 6 and board[x][y-2] is None:
                possibleMoves.append((x, y-2))
            possibleMoves.append((x, y-1))

        #Attack        
        if x-1 >= 0 and board[x-1][y-1] is not None and board[x-1][y-1].Color != self.Color:
            possibleMoves.append((x-1, y-1))
        if x+1 < 8 and board[x+1][y-1] and board[x+1][y-1].Color != self.Color:
            possibleMoves.append((x+1, y-1))

        return possibleMoves

    def toString(self):
        if self.Color == 0:
            return "White Pawn"
        else:
            return "Black Pawn"



class King(chessPiece):

    def __init__(self, Color, x, y):
        super().__init__(Color, x, y)

    def returnMoves(self, board):
        possibleMoves = []
        x, y = self.Location

        if x-1 >= 0:
            possibleMoves.append((x-1, y))
            if y - 1 >= 0:
                possibleMoves.append((x-1, y-1))
            if y + 1 < 8:
                possibleMoves.append((x-1, y+1))
        if x+1 < 8:
            possibleMoves.append((x+1, y))
            if y - 1 >= 0:
                possibleMoves.append((x+1, y-1))
            if y + 1 < 8:
                possibleMoves.append((x+1, y+1))
        if y - 1 >= 0:
            possibleMoves.append((x, y-1))
        if y + 1 < 8:
            possibleMoves.append((x, y+1))
        
        movesToDelete = []

        for move in possibleMoves:
            newX, newY = move
            if board[newX][newY] is not None and board[newX][newY].Color == self.Color:
                movesToDelete.append(move)

        for move in movesToDelete:
            possibleMoves.remove(move)

        #Castle
        if y == 7 and x == 4:
            if board[0][7] is not None and isinstance(board[0][7], Rook):
                if board[1][7] is None and board[2][7] is None and board[3][7] is None:
                    possibleMoves.append((1, 7))
            if board[7][7] is not None and isinstance(board[7][7], Rook):
                if board[5][7] is None and board[6][7] is None:
                    possibleMoves.append((6, 7))

        return possibleMoves
    
    def toString(self):
        if self.Color == 0:
            return "White King"
        else:
            return "Black King"