from PySide2.QtWidgets import QApplication
from qtmodern.styles import dark

from gui.visualizerwindow import VisualizerWindow
import gui.rc.icons_rc as icons_rc  # Although this doesn't seem to be used, it is necessary for icons to show up


if __name__ == '__main__':
    app = QApplication()
    dark(app)

    window = VisualizerWindow()

    size = app.desktop().size()
    window.setMinimumSize(size.width()*2/3, size.height()*2/3)

    window.showMaximized()

    exit(app.exec_())
