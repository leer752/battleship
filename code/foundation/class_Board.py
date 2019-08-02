

# Create a class object that represents the board
# __init__ function defines whether the space belongs to an enemy or player, which ship the unit belongs to,
# the color of the square, the x & y positions of the square, and the rectangle dimensions for the square
class Board(object):
    def __init__(self, alignment, color, status, number, rectangle):
        self.alignment = alignment
        self.number = number
        self.status = status
        self.color = color
        self.rectangle = rectangle
