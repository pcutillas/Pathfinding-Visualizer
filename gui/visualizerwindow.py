from PySide2.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide2.QtGui import QIcon

from gui.ui.ui_mainwindow import Ui_MainWindow
from gui.cell import Cell
from data.node import Node
import data.algorithms as algs


class VisualizerWindow(QMainWindow):
    """
    The main window of this application
    """

    instance = None

    def __init__(self):

        # Initialize superclass
        QMainWindow.__init__(self)
        self.setWindowIcon(QIcon(':/icon/icons/app.ico'))

        # Setup the UI defined in Qt Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Generate the grid that will be interacted with
        self.numRows = 29  # Odd so that starting points are vertically centered
        self.numCols = 60
        self._setupGrid()

        # Define the start and end nodes
        self.start = Node.GRID[round(self.numRows/2)][8]
        self.end = Node.GRID[round(self.numRows/2)][-8]
        self.setStartNode(self.start)
        self.setEndNode(self.end)

        # -- User interaction variables --
        # Click & dragging
        self.changingStart = False  # Changing start node
        self.changingEnd = False  # Changing end node
        self.drawingWall = False  # Drawing a new wall
        self.erasingWall = False  # Deleting walls

        # Connecting button signals to functions
        self.connectSignals()
        self.ui.speedSlider.setValue(29)

        # Populate the algorithm dropdown
        self.populateDropdown()

        VisualizerWindow.instance = self

    def reset(self):
        """
        Resets the grid to its original state
        """

        for x in range(self.numRows):
            for y in range(self.numCols):
                cell = Node.GRID[x][y].cell
                cell.clear()
                cell.setWall(False)

        self.start.cell.clear()
        self.end.cell.clear()
        self.start.isStart = False
        self.end.isEnd = False

        self.start = Node.GRID[round(self.numRows / 2)][8]
        self.end = Node.GRID[round(self.numRows / 2)][-8]
        self.setStartNode(self.start)
        self.setEndNode(self.end)

    def _setupGrid(self):
        """
        Generates the grid of Cells along with the underlying Nodes that are used to visualize the selected algorithm
        """

        # First, generate the grid
        for x in range(self.numRows):
            for y in range(self.numCols):

                # Make the visual Cell representing the Node at x, y, then add it visually at those coordinates
                cell = Cell(Node(x, y), self)
                self.ui.gridLayout.addWidget(cell, x, y)

        # Then reiterate and populate the neighbors, with diagonals enabled by default
        self.populateNeighbors()

    def populateNeighbors(self, withDiagonals: bool = True):
        """
        Populates all Nodes' neighbors
        """

        for x in range(self.numRows):
            for y in range(self.numCols):
                Node.GRID[x][y].populateNeighbors(withDiagonals)

    def setStartNode(self, node: Node):
        """
        Sets node as the start node and updates the GUI with it too
        """
        if not node.isEnd:
            self.start.isStart = False
            node.isStart = True

            self.start.cell.draw(Cell.EMPTY)

            self.start = node
            node.cell.setStart()

    def setEndNode(self, node: Node):
        """
        Sets node as the end node and updates the GUI with it too
        """
        if not node.isStart:
            self.end.isEnd = False
            node.isEnd = True

            self.end.cell.draw(Cell.EMPTY)

            self.end = node
            node.cell.setEnd()

    def mouseReleaseEvent(self, event):
        """
        Performs the actions necessary depending on what the user was doing with their click.
        NOTE: The mouse press events are handled by the Cells
        """

        cell = self.childAt(event.pos())  # Not guaranteed that this is actually a cell yet

        if self.changingStart:
            QApplication.restoreOverrideCursor()
            self.changingStart = False

            # Check that it is a cell and that it isn't either of the start or end nodes
            if isinstance(cell, Cell) and not (cell.node.isEnd or cell.node.isStart):
                cell.setWall(False)
                self.setStartNode(cell.node)
            else:
                self.setStartNode(self.start)

        elif self.changingEnd:
            QApplication.restoreOverrideCursor()
            self.changingEnd = False

            # Check that it is a cell and that it isn't either of the start or end nodes
            if isinstance(cell, Cell) and not (cell.node.isEnd or cell.node.isStart):
                cell.setWall(False)
                self.setEndNode(cell.node)
            else:
                self.setEndNode(self.end)

        elif self.erasingWall:
            self.erasingWall = False

        elif self.drawingWall:
            self.drawingWall = False

    def mouseMoveEvent(self, event):
        """
        Determines if the dragging is to make a wall or to remove it
        """

        if self.drawingWall:
            # Get widget at that position
            cell = self.childAt(event.pos())

            # Check that it is a cell and that it isn't either of the start or end nodes
            if isinstance(cell, Cell) and not (cell.node.isEnd or cell.node.isStart):
                cell.setWall(True)

        elif self.erasingWall:
            # Similar to above
            cell = self.childAt(event.pos())
            if isinstance(cell, Cell) and not (cell.node.isEnd or cell.node.isStart):
                cell.setWall(False)

    def clearPastVisual(self):
        """
        Clears the visual that was last run
        """

        for x in range(self.numRows):
            for y in range(self.numCols):
                node = Node.GRID[x][y]

                # A*
                node.f = node.g = node.h = None

                if node.wall:
                    continue
                node.cell.draw(Cell.EMPTY)

                if node.isStart:
                    node.cell.setStart()
                elif node.isEnd:
                    node.cell.setEnd()

    def loadHeuristics(self, algIndex: int):
        """
        Loads the heuristics dropdown with appropriate heuristics
        """

        # Clear heuristics box
        box = self.ui.heuristicBox
        box.clear()

        # Get applicable heuristics
        heuristics = self.ui.algorithmBox.itemData(algIndex)['heuristics']

        # Repopulate heuristic dropdown
        for h in heuristics:
            box.addItem(h, algs.HEURISTICS.get(h, None))

    def runSelectedAlgorithm(self):
        """
        Runs the algorithm currently selected in the dropdown menu
        """

        self.clearPastVisual()

        algorithm = self.ui.algorithmBox.currentData()['algorithm']
        heuristic = self.ui.heuristicBox.currentData()

        pathFound = algorithm(self.start, self.end, heuristic)

        if not pathFound:
            QMessageBox.warning(self, 'No Path Found', 'No paths were found.')

    def populateDropdown(self):
        """
        Populates the dropdown with the list of supported algorithms

        Each algorithm will have associated data of the form:
        { 'algorithm': algorithmFunction, 'heuristics': [h1Name, h2Name, ...] }
        """

        icon = QIcon(":/icon/icons/app.ico")

        # A Star
        self.ui.algorithmBox.addItem(
            icon, "A*",
            userData=
            {
                'algorithm': algs.aStar,
                'heuristics': ['Manhattan']
            }
        )

    def connectSignals(self):
        """
        Connects all necessary signals from GUI elements to their respective functions
        """

        self.ui.resetButton.clicked.connect(self.reset)
        self.ui.allowDiagonals.toggled.connect(self.populateNeighbors)

        def changeSpeed(val):
            # val ranges from 0 to 99. at 99, slowdown is .001, and at 0, .1
            algs.slowdown = .5 / (val+1)

        self.ui.speedSlider.valueChanged.connect(changeSpeed)

        self.ui.algorithmBox.currentIndexChanged.connect(self.loadHeuristics)
        self.ui.goButton.clicked.connect(self.runSelectedAlgorithm)

