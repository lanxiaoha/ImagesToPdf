from PyQt5.QtWidgets import QApplication
from src.page.MainPageWindow import MainPageWindow
import sys

if __name__ == '__main__':
    appctxt = QApplication([])       # 1. Instantiate ApplicationContext
    mainWindow = MainPageWindow()
    mainWindow.show()
    exit_code = appctxt.exec()    # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
