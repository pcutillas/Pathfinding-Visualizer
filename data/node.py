from gui.cell import Cell


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
        self.isStart = self.isEnd = False

        # For A*
        self.f = self.g = self.h = None

        # Add to array
        if len(Node.GRID) - 1 < x:
            Node.GRID.append([])
        Node.GRID[x].append(self)

        self.wall = False  # Whether or not this node is a wall
        self.cell = None  # The Cell tied to this Node

    def setCell(self, cell):
        self.cell = cell

    def inPath(self):
        # A pass-through to cell's inPath method
        self.cell.inPath()

    def inList(self):
        self.cell.draw(Cell.IN_LIST)

    def searched(self):
        # A pass-through to cell's searched method
        self.cell.searched()

    def populateNeighbors(self, withDiagonals: bool):
        """
        Populates the neighbors variable with this node's neighbors.
        """
        self.neighbors = []

        relativePositions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # The 4 Nodes directly adjacent to self

        if withDiagonals:
            relativePositions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # The 4 diagonal Nodes

        for relPos in relativePositions:

            row = self.x + relPos[0]
            col = self.y + relPos[1]

            # Check boundaries
            if 0 <= row < len(Node.GRID) and 0 <= col < len(Node.GRID[0]):
                self.neighbors.append(Node.GRID[row][col])

    def isAdjacentTo(self, node):
        """
        Returns true if nodes are adjacent, otherwise false
        """

        if node not in self.neighbors:
            return False

        return (self.x == node.x and self.y == node.y + 1) or (self.x == node.x and self.y == node.y - 1) or \
            (self.x == node.x + 1 and self.y == node.y) or (self.x == node.x - 1 and self.y == node.y)

    def __repr__(self):
        # Used for printing the node when debugging
        return f'({self.x}, {self.y})'
