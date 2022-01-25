class Piece:
    def __init__(self, white):
        self._white = white
        self._firstMove = True
    def move(self):
        self._firstMove = False
    def isFirstMove(self):
        return self._firstMove
    def isWhite(self):
        return self._white
    # Start and to is tuple like (2,3) and define the board location
    def isValid(self, start, to):
        # return moving possibility and path checking list
        pass
    def capture(self, start, to):
        # return moving possibility and path checking list for capturing
        # In some pieces it may different from isValid methode
        pass
    def possibleMoves(self, start):
        # return all of the possible moves of a piece
        pass

class King(Piece):
    def __init__(self, white):
        Piece.__init__(self, white)
    def move(self):
        Piece.move(self)

    def isValid(self, start, to):
        # king can only move around one unit
        if abs(start[0] - to[0]) <=1 and abs(start[1] - to[1]) <=1:
            return True, []
        return False, []

    def capture(self, start, to):
        return self.isValid(start, to)

    def possibleMoves(self, start):
        lst = []
        for i in range(-1,2):
            for j in range(-1, 2):
                lst.append((start[0]+i, start[1]+j))
        out = []
        for a in lst:
            if 0 <= a[0] < 8 and 0 <= a[1] < 8 and a!=start:
                out.append(a)
        return out

    def __str__(self):
        if self.isWhite():
            return "K"
        else:
            return "k"


class Queen(Piece):
    def __init__(self, white):
        Piece.__init__(self, white)
    def move(self):
        Piece.move(self)

    def isValid(self, start, to):
        # Checking Diagonal movement
        if abs(start[0]-to[0])==abs(start[1]-to[1]):
            pathChecking = []
            x = int(-1*(start[0]-to[0])/abs(start[0]-to[0]))
            y = int(-1*(start[1]-to[1])/abs(start[1]-to[1]))
            for i in range(1,abs(start[0]-to[0])):
                pathChecking.append((start[0]+(i*x), start[1]+(i*y)))
            return True, pathChecking
        # Checking Vertical movement
        if start[0] ==to[0]:
            pathChecking = []
            y = int(-1*(start[1] - to[1]) / abs(start[1] - to[1]))
            for i in range(1,abs(start[1]-to[1])):
                pathChecking.append((start[0], start[1]+(i*y)))
            return True, pathChecking
        # Checking Horizontal movement
        if start[1]==to[1]:
            pathChecking = []
            x = int(-1*(start[0]-to[0])/abs(start[0]-to[0]))
            for i in range(1, abs(start[0] - to[0])):
                pathChecking.append((start[0]+(i*x), start[1]))
            return True, pathChecking
        return False, []
    def capture(self, start, to):
        return self.isValid(start, to)
    def possibleMoves(self, start):
        lst = []
        for i in range(0, 8):
            lst.append((i, start[1]))
        for j in range(0, 8):
            if j!=start[1]:
                lst.append((start[0], j))
        for i in range(-7, 8):
            lst.append((start[0]+i, start[1]+i))
            lst.append((start[0]-i, start[1]+i))
        out = []
        for a in lst:
            if 0 <= a[0] < 8 and 0 <= a[1] < 8 and a!=start:
                out.append(a)
        return out

    def __str__(self):
        if self.isWhite():
            return "Q"
        else:
            return "q"

class Rook(Piece):
    def __init__(self, white):
        Piece.__init__(self, white)
    def move(self):
        Piece.move(self)

    def isValid(self, start, to):
        # Checking Vertical movement
        if start[0]==to[0]:
            pathChecking = []
            y = int(-1*(start[1] - to[1]) / abs(start[1] - to[1]))
            for i in range(1,abs(start[1]-to[1])):
                pathChecking.append((start[0], start[1]+(i*y)))
            return True, pathChecking
        # Checking Horizontal movement
        if start[1]==to[1]:
            pathChecking = []
            x = int(-1*(start[0]-to[0])/abs(start[0]-to[0]))
            for i in range(1, abs(start[0] - to[0])):
                pathChecking.append((start[0]+(i*x), start[1]))
            return True, pathChecking
        return False, []
    def capture(self, start, to):
        return self.isValid(start, to)

    def possibleMoves(self, start):
        lst = []
        for i in range(0, 8):
            lst.append((i, start[1]))
        for j in range(0, 8):
            if j!=start[1]:
                lst.append((start[0], j))
        out = []
        for a in lst:
            if 0 <= a[0] < 8 and 0 <= a[1] < 8 and a!=start:
                out.append(a)
        return out
    def __str__(self):
        if self.isWhite():
            return "R"
        else:
            return "r"

class Bishop(Piece):
    def __init__(self, white):
        Piece.__init__(self, white)
    def move(self):
        Piece.move(self)

    def isValid(self, start, to):
        # Checking Diagonal movement
        if abs(start[0]-to[0])==abs(start[1]-to[1]):
            pathChecking = []
            x = int(-1*(start[0]-to[0])/abs(start[0]-to[0]))
            y = int(-1*(start[1]-to[1])/abs(start[1]-to[1]))
            for i in range(1,abs(start[0]-to[0])):
                pathChecking.append((start[0]+(i*x),start[1]+(i*y)))
            return True, pathChecking
        return False, []
    def capture(self, start, to):
        return self.isValid(start, to)

    def possibleMoves(self, start):
        lst = []
        for i in range(-7, 8):
            lst.append((start[0]+i, start[1]+i))
            lst.append((start[0]-i, start[1]+i))
        out = []
        for a in lst:
            if 0 <= a[0] < 8 and 0 <= a[1] < 8 and a!=start:
                out.append(a)
        return out
    def __str__(self):
        if self.isWhite():
            return "B"
        else:
            return "b"
class Knight(Piece):
    def __init__(self, white):
        Piece.__init__(self, white)
    def move(self):
        Piece.move(self)

    def isValid(self, start, to):

        if abs(start[0]-to[0]) == 2 and abs(start[1]-to[1]) == 1:
            return True, []
        if abs(start[0]-to[0]) == 1 and abs(start[1]-to[1]) == 2:
            return True, []
        return False, []
    def capture(self, start, to):
        return self.isValid(start, to)

    def possibleMoves(self, start):
        lst = []
        for i in [-1, 1]:
            for j in [-2, 2]:
                lst.append((start[0]+i, start[1]+j))
                lst.append((start[0]+j, start[1]+i))
        out = []
        for a in lst:
            if 0 <= a[0] < 8 and 0 <= a[1] < 8 and a!=start and a not in out:
                out.append(a)
        return out
    def __str__(self):
        if self.isWhite():
            return "N"
        else:
            return "n"
class Pawn(Piece):
    def __init__(self, white):
        Piece.__init__(self, white)
    def move(self):
        Piece.move(self)

    def isValid(self, start, to):
        y=-1
        if self.isWhite():
            y=1

        if start[0]==to[0] and to[1]-start[1]==y:
            return True, []
        #Pawn can move forward two cells in the first movement
        if start[0]==to[0] and to[1]-start[1]==2*y and self.isFirstMove():
            return True, [(start[0], start[1]+y)]

        return False, []
    def capture(self, start, to):
        y=-1
        if self.isWhite():
            y=1
        if abs(start[0]-to[0])==1 and to[1]-start[1]==y:
            return True, []
        return False, []
    def possibleMoves(self, start):
        y=-1
        if self.isWhite():
            y=1
        lst = [(start[0], start[1]+y), (start[0], start[1]+(2*y)), (start[0]+1, start[1]+y), (start[0]-1, start[1]+y)]
        out = []
        for a in lst:
            if 0 <= a[0] < 8 and 0 <= a[1] < 8:
                out.append(a)
        return out

    def __str__(self):
        if self.isWhite():
            return "P"
        else:
            return "p"
