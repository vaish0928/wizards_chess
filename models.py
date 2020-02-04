
class Location (object):
    def __init__ (self, piece, color):
        self.piece = piece
        self.color = color


class Player (object):
    def __init__(self, color):
        self.name = 'default'
        self.color = color
        self.activePieces = []
        self.lostPieces = []
        self.takenPieces = []

    def setName(self, text):
        self.name = text
