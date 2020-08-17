

class Node:
    """
    The data representation of a node
    """

    GRID = []

    def __init__(self, x, y, previous=None):
        self.x = x
        self.y = y
        self.previous = previous
        self.neighbors = []  # Gets populated once grid is fully populated too
        self.isStart = False
        self.isEnd = False

        # For A*
        self.f = self.g = self.h = 0

        # Add to array
        if len(Node.GRID) - 1 < x:
            Node.GRID.append([])
        Node.GRID[x].append(self)

        self.wall = False  # Whether or not this node is a wall
        self.cell = None  # The Cell tied to this Node

    def setCell(self, cell):
        self.cell = cell

    def populateNeighbors(self):
        """
        Populates the neighbors variable with this node's neighbors.
        """

        for relPos in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            row = self.x + relPos[0]
            col = self.y + relPos[1]

            # Check boundaries
            if 0 <= row < len(Node.GRID) and 0 <= col < len(Node.GRID[0]):
                self.neighbors.append(Node.GRID[row][col])
