from PyQt5.QtWidgets import QApplication
import sys
from  src.page.MainPageWindow import MainPageWindow

if __name__ == '__main__':
    appContext = QApplication([])
    mainWindow = MainPageWindow()
    mainWindow.show()
    exitCode = appContext.exec()
    sys.exit(exitCode)