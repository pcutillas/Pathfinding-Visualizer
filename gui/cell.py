from PySide2.QtWidgets import QSizePolicy, QLabel, QApplication
from PySide2.QtGui import QColor, QPalette, QPixmap, QCursor, Qt


class Cell(QLabel):
    """
    The visual representation of a Node
    """

    EMPTY = QColor(0, 0, 0, 120)
    JUST_SEARCHED = QColor(0, 0, 0)
    JUST_SEARCHED_2 = QColor(0, 0, 0)
    SEARCHED = QColor(250, 0, 0)
    PATH = QColor(255, 255, 255)
    WALL = QColor(255, 255, 255, 100)

    def __init__(self, node, mainWindow):
        # Init superclass
        QLabel.__init__(self)

        self.mainWindow = mainWindow
        self.node = node
        node.setCell(self)

        # -- Getting expected GUI behavior --
        self.setAutoFillBackground(True)  # Allows for automatic color updating
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)  # Allows cells to adapt to window size
        self.setScaledContents(True)  # Makes images scale to cell size
        self.setAttribute(Qt.WA_Hover, True)  # Allows the enterEvent definition to work

        # Initialize as empty cell
        self.draw(Cell.EMPTY)

    def draw(self, color: QColor):
        """
        Draws this cell with the specified color. The class variables will be passed in, but any color can be used
        """

        pal = QPalette()
        pal.setColor(QPalette.Background, color)
        self.setPalette(pal)

    def setStart(self):
        """
        Draws this cell as the start node
        """
        self.setPixmap(QPixmap(":/icon/icons/start.png"))

    def setEnd(self):
        """
        Draws this cell as the end node
        """
        self.setPixmap(QPixmap(":/icon/icons/end.png"))

    def setWall(self, wall: bool):
        """
        Draws this cell as a wall and updates the node to reflect it
        """
        if wall:
            self.draw(Cell.WALL)
            self.node.wall = True
        else:
            self.draw(Cell.EMPTY)
            self.node.wall = False

    def mousePressEvent(self, event):
        """
        Determines if self is the start or end node or neither, and updates things accordingly
        NOTE: The mouse release event is handled by the window
        """

        if self.node.isStart:
            QApplication.setOverrideCursor(QCursor(QPixmap(":/icon/icons/start.png").scaledToHeight(self.height())))
            self.clear()
            self.draw(Cell.EMPTY)
            self.mainWindow.changingStart = True
        elif self.node.isEnd:
            QApplication.setOverrideCursor(QPixmap(":/icon/icons/end.png").scaledToHeight(self.height()))
            self.clear()
            self.draw(Cell.EMPTY)
            self.mainWindow.changingEnd = True
        elif self.node.wall:
            self.mainWindow.erasingWall = True
            self.setWall(False)
        else:
            self.mainWindow.drawingWall = True
            self.setWall(True)
