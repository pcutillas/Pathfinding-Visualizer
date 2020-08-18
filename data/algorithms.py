from PySide2.QtCore import QEventLoop, QTimer
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication
from time import sleep


slowdown = 0


def aStar(startNode, endNode):
    """
    Runs an A Star algorithm to find the shortest path between the startNode and endNode.
    Uses the Manhattan Distance heuristic
    Returns True if the path was found, otherwise returns False
    """

    # define the open and closed lists (open list starts with start node)
    openList, closedList = [startNode], []

    # Iterate until list is empty
    while len(openList):

        # Sort the open list to put nodes with lowest cost (f) at beginning
        openList.sort(key=lambda n: n.f)

        # Get the lowest-cost node and add to closed list
        closedList.append(curNode := openList.pop(0))
        curNode.searched()
        sleep(slowdown)

        # Refresh GUI (Called elsewhere too)
        QApplication.processEvents()

        # If we found the end node, draw the path and return True
        if curNode is endNode:
            path = []

            while curNode is not startNode:  # Iterates back to the start node
                path.append(curNode)
                curNode = curNode.previous
            path.append(startNode)

            # Draw path with a delay to somewhat animate it
            for node in reversed(path):
                node.inPath()
                QApplication.processEvents()
                sleep(slowdown*3)

            return True

        # Now add the neighboring nodes if they aren't walls or already closed
        for node in curNode.neighbors:
            if node.wall:
                continue

            if node in closedList:
                continue

            # Calculate g
            # g = curNode.g + 1 if curNode.g is not None else 0
            g = abs(node.x - startNode.x) + abs(node.y - startNode.y)

            # Calculate h using heuristic
            h = abs(node.x - endNode.x)**2 + abs(node.y - endNode.y)**2

            # Add to get f
            f = g + h

            # Check current f value of node. If higher than calculation, use new,
            #  lower value to represent node and change previous node too
            if node.f is None or f < node.f:

                # Assign values to node
                node.g, node.h, node.f = g, h, f

                # Avoids circular loops
                node.previous = curNode

                # Add to open list only if it isn't there already
                if node not in openList:
                    openList.append(node)
                    node.inList()
                    QApplication.processEvents()

    # If it gets here, no path was found
    return False
