import Board
import re

class Game:
    def __init__(self):
        self._whiteTurn = True
        self._board = Board.Board()
        self.gameStart()

    # this method starts the game and handle moving
    def gameStart(self):
        # game run in this while loop until one player become mate
        while(True):
            string = input(self._board.turnToString(self._whiteTurn)+" turn: ")
            valid, start, to = self._inputAnalysis(string)
            # check validity of user input
            if valid:
                # if user input be a correct move syntax moving process will start
                res = self._board.move(start, to, self._whiteTurn)
                if res == "mate":
                    # in the case of mate
                    exit()
                elif res == "promotion":
                    # in the case of pawn promotion
                    print("You can promote your pawn to Queen, Rook, Knight, Bishop")
                    change = input("Please input your desire Piece: ")
                    changeAck = self._board.promotion(to, change, self._whiteTurn)
                    while not changeAck:
                        # this while execute until valid input
                        change = input("Please input Correct Piece: ")
                        changeAck = self._board.promotion(to, change, self._whiteTurn)
                    # check the checkmate situation of other player after the promotion
                    if self._board.isCheckMate(not self._whiteTurn):
                        print(self._board.turnToString(not self._whiteTurn) + " is Checkmate!")
                        exit()
                    else:
                        self._whiteTurn = not self._whiteTurn
                elif res:
                    # changing the turn after every correct move
                    self._whiteTurn = not self._whiteTurn
                else:
                    print("Please enter valid move!")

    # chang the standard format of chess input into the our implementation positions
    def _getPositions(self, string):
        p = re.compile('[a-z][1-9]')
        matches = p.finditer(string)
        result = []
        for match in matches:
            result.append(self._posRE(string[match.start():match.end()]))
        return result

    # change chess string to position like c3 to 2,2
    @staticmethod
    def _posRE(string):
        x = ord(string[0]) - ord('a')
        y = int(string[1]) - 1
        return x, y

    # analysing user input
    def _inputAnalysis(self, string):
        p = re.compile('[a-z][1-9][a-z][1-9]')
        match = p.match(string)
        if match is not None and len(string)==4:
            out = self._getPositions(string)
            start = out[0]
            to = out[1]
            # Bounder checking
            if start[0] >= 8 or start[0] < 0 or start[1] >= 8 or start[1] < 0:
                print("Your select is out of the bound")
                return False, 0, 0
            if to[0] >= 8 or to[0] < 0 or to[1] >= 8 or to[1] < 0:
                print("Your goal is out of the bound")
                return False, 0, 0
            return True, start, to
        elif string=="reset":
            # reset game
            return False, 0, 0
        elif string=="exit":
            exit()
        elif string == "print":
            print(self._board)
            return False, 0, 0
        else:
            print("please input correct!")
            return False, 0, 0



