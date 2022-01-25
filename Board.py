import Piece
from copy import deepcopy

class Board:
    def __init__(self):
        self.height = 8
        self.width = 8

        self.captured = []
        self._board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(Spot((i, j)))
            self._board.append(row)
        self._initPieces()

    def _initPieces(self):
        for i in [0, 7]:
            self._board[0][i].setPiece(Piece.Rook(i==0))
            self._board[1][i].setPiece(Piece.Knight(i==0))
            self._board[2][i].setPiece(Piece.Bishop(i==0))
            self._board[3][i].setPiece(Piece.Queen(i==0))
            self._board[4][i].setPiece(Piece.King(i==0))
            self._board[5][i].setPiece(Piece.Bishop(i==0))
            self._board[6][i].setPiece(Piece.Knight(i==0))
            self._board[7][i].setPiece(Piece.Rook(i==0))

        for j in [1, 6]:
            for i in range(8):
                self._board[i][j].setPiece(Piece.Pawn(j==1))

    # check whether a move is castling move in board
    def isCastling(self, start, to):
        piece = self.getPiece(start)
        if isinstance(piece, Piece.King) and piece.isFirstMove() and (to[0] == 2 or to[0] == 6) and to[1]==start[1]:
            return True
        else:
            return False

    # do castling according to its rul and board
    def doCastling(self, start, to, white):
        if to[0] == 2:
            rookSpot = self.getSpot((0, to[1]))
            if rookSpot.isEmpty():
                return False
            rook = rookSpot.getPiece()
            if not isinstance(rook, Piece.Rook):
                return False
            if not rook.isFirstMove():
                return False
            isValid = self.isValid(rookSpot.getPosition(), (start[0]-1, start[1]),white)
            if not isValid:
                return False
            spot1 = self.getSpot((start[0]-1, start[1]))
            spot2 = self.getSpot((start[0]-2, start[1]))
            if self.inDanger(spot1.getPosition(), white) or self.inDanger(spot2.getPosition(), white):
                return False
            kingSpot = self.getSpot(start)
            king = kingSpot.getPiece()
            kingSpot.setPiece(None)
            newKingSpot = self.getSpot(to)
            newRookSpot = self.getSpot((start[0]-1, start[1]))
            newKingSpot.setPiece(king)
            rookSpot.setPiece(None)
            newRookSpot.setPiece(rook)
            newRookSpot.getPiece().move()
            newKingSpot.getPiece().move()
            return True
        else:
            rookSpot = self.getSpot((7, to[1]))
            if rookSpot.isEmpty():
                return False
            rook = rookSpot.getPiece()
            if not isinstance(rook, Piece.Rook):
                return False
            if not rook.isFirstMove():
                return False
            isValid = self.isValid(rookSpot.getPosition(), (start[0] + 1, start[1]), white)
            if not isValid:
                return False
            spot1 = self.getSpot((start[0]+1, start[1]))
            spot2 = self.getSpot((start[0]+2, start[1]))
            if self.inDanger(spot1.getPosition(), white) or self.inDanger(spot2.getPosition(), white):
                return False
            kingSpot = self.getSpot(start)
            king = kingSpot.getPiece()
            kingSpot.setPiece(None)
            newKingSpot = self.getSpot(to)
            newRookSpot = self.getSpot((start[0]+1, start[1]))
            newKingSpot.setPiece(king)
            rookSpot.setPiece(None)
            newRookSpot.setPiece(rook)
            newRookSpot.getPiece().move()
            newKingSpot.getPiece().move()
            return True

    @staticmethod
    def turnToString(white):
        if white:
            return "White"
        else:
            return "Black"

    # check after a move whether that was a pawn promotion situation
    def _isPromotion(self, to, white):
        spot = self.getSpot(to)
        piece = spot.getPiece()
        if isinstance(piece, Piece.Pawn) and white and to[1]==7:
            return True
        if isinstance(piece, Piece.Pawn) and not white and to[1]==0:
            return True
        return False

    # do promotion according to the user desire piece
    def promotion(self, position, piece, white):
        if piece == "Queen":
            newP = Piece.Queen(white)
        elif piece == "knight":
            newP = Piece.Knight(white)
        elif piece == "Rook":
            newP = Piece.Rook(white)
        elif piece == "Bishop":
            newP = Piece.Bishop(white)
        else:
            return False
        spot = self.getSpot(position)
        spot.setPiece(newP)
        return True

    # this is main method for moving a piece and it check validity and change pieces positions
    def move(self, start, to, white):
        # first we check whether its a castling move
        if self.isCastling(start, to):
            print("Castling!")
            return self.doCastling(start, to, white)
        # then check if it is a valid move due to the piece rul and board
        elif self.isValid(start, to, white):
            # we clone current situation, because in case of invalid move we must back to this situation
            copyBoard = deepcopy(self._board)
            isCheck = self.isCheck(white)
            d_spot= self.getSpot(to)
            s_spot= self.getSpot(start)
            # if a piece present in destiny spot in should be capture
            if not d_spot.isEmpty():
                self.captured.append(d_spot.getPiece())
            d_spot.setPiece(s_spot.getPiece())
            s_spot.setPiece(None)
            # after a valid if player become check we reverse the move and he should change his move
            if self.isCheck(white):
                if isCheck:
                    print("You are checked!")
                else:
                    # in case of moving a piece and open a path to your king
                    print("By moving this piece, you become check!")
                self._board = copyBoard
                return False
            # by calling move() method of a piece we only change the firstMove parameter
            d_spot.getPiece().move()
            # check for promotion situation
            if self._isPromotion(to, white):
                return "promotion"
            # check if other player become mate after a move
            if self.isCheckMate(not white):
                print(self.turnToString(not white)+ " is Checkmate!")
                return "mate"
            return True
        else:
            return False

    def setPiece(self, position, piece):
        self._board[position[0]][position[1]].setPiece(piece)

    def getPiece(self, position):
        return self._board[position[0]][position[1]].getPiece()

    def getSpot(self, position):
        return self._board[position[0]][position[1]]

    # check other player can capture a position
    def inDanger(self, position, white):
        slist = self.getSpotsList(not white)
        for spot in slist:
            piece = spot.getPiece()
            isValid, lst = piece.capture(spot.getPosition(), position)
            if isValid and self.pathChecking(lst):
                return True
        return False

    # check whether a king is in danger of other player pieces
    def isCheck(self, white):
        king = self.getKingSpot(white)
        return self.inDanger(king.getPosition(), white)

    # check whether a player is checkmate
    def isCheckMate(self, white):
        # if somebody is checkmate, he should checked
        if not self.isCheck(white):
            return False
        # first we get all of available player spot with a piece
        slist = self.getSpotsList(white)
        for spot in slist:
            # then play every possible and valid move
            piece = spot.getPiece()
            moveList = piece.possibleMoves(spot.getPosition())
            for to in moveList:
                if self.isValid(spot.getPosition(), to, white):
                    copyBoard = deepcopy(self._board)
                    d_spot = self.getSpot(to)
                    s_spot = self.getSpot(spot.getPosition())
                    if not d_spot.isEmpty():
                        self.captured.append(d_spot.getPiece())
                    d_spot.setPiece(s_spot.getPiece())
                    s_spot.setPiece(None)
                    if self.isCheck(white):
                        # if after a move it still check, reverse the move to current situation
                        self._board = copyBoard
                    else:
                        # if we can find a valid move that exit player from check, its not checkmate
                        self._board = copyBoard
                        return False
        # if there is no other move that can prevent the check situation its a checkmate situation
        return True

    # searching in every spot for king piece
    def getKingSpot(self, white):
        for row in self._board:
            for spot in row:
                if not spot.isEmpty():
                    if spot.getPiece().isWhite() == white:
                        if isinstance(spot.getPiece(), Piece.King):
                            return spot

    # this method return every spot that consist one player pieces
    def getSpotsList(self, white):
        slist = []
        for row in self._board:
            for spot in row:
                if not spot.isEmpty():
                    if spot.getPiece().isWhite() == white:
                        slist.append(spot)
        return slist

    # this method check every aspect of a valid move in chess and return True or False
    def isValid(self, start, to, white):
        # Bounder checking
        if start[0] >= self.width or start[0] < 0 or start[1] >= self.height or start[1] < 0:
            # print("Your select is out of the bound")
            return False
        if to[0] >= self.width or to[0] < 0 or to[1] >= self.height or to[1] < 0:
            # print("Your goal is out of the bound")
            return False

        spot = self.getSpot(start)
        if spot.isEmpty():
            # print("Please select a piece")
            return False

        piece = spot.getPiece()
        if piece.isWhite()!=white:
            # print("Please select your piece")
            return False

        destination = self.getSpot(to)
        if not destination.isEmpty():
            d_piece = destination.getPiece()
            if d_piece.isWhite()==white:
                # print("Please select empty destination!")
                return False
            else:
                # Capturing situation
                isValid, lst = piece.capture(start, to)
                if isValid and self.pathChecking(lst):
                    return True
                else:
                    # print("It is invalid move!")
                    return False

        else:
            # Normal moving
            isValid, lst = piece.isValid(start, to)
            if isValid and self.pathChecking(lst):
                return True
            else:
                # print("It is invalid move!")
                return False

    # this method check path of a piece because every spot in the its path should be free
    def pathChecking(self, lst):
        for des in lst:
            if self.getPiece(des) is not None:
                return False
        return True

    def __str__(self):
        out = ""
        for j in range(self.height):
            for i in range(self.width):
                out += " " + str(self._board[i][self.height-j-1])
            out += "\n"
        return out

# our chess board consist of 64 spot which keep a position and a piece
class Spot:
    def __init__(self, position, piece=None):
        self._position = position
        self._piece = piece
    def isEmpty(self):
        return self._piece is None

    def getPosition(self):
        return self._position
    def setPiece(self, piece):
        self._piece= piece
    def getPiece(self):
        return self._piece
    def __str__(self):
        if self.isEmpty():
            return "-"
        else:
            return str(self._piece)

