from PyQt5.QtWidgets import  QMainWindow,QFileDialog,QMessageBox
from .ui.ImagesToPdfMainWindow import Ui_ImageToPdfWindow
import os
from PyQt5.QtGui import QDoubleValidator
from .ImageToPdf import exportPdfFile

class MainPageWindow(QMainWindow,Ui_ImageToPdfWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("图片列表转pdf")
        self.setFixedSize(self.width(),self.height())
        self.foldPath:str = ""
        self.scale = 1.5
        self.initListener()

    def initListener(self):
        self.startButton.clicked.connect(self.onClickStart)
        self.selectFoldButton.clicked.connect(self.openFoldDialog)
        self.scaleEdit.setValidator(QDoubleValidator())

    def openFoldDialog(self):
        dialog:QFileDialog = QFileDialog()
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setFileMode(QFileDialog.FileMode.DirectoryOnly)
        if(dialog.exec()):
            foldPath = dialog.selectedFiles()
            if foldPath:
                self.onFoldPathSelected(foldPath[0])

    def onFoldPathSelected(self,foldPath):
        print("fold",foldPath)
        self.foldPath = foldPath
        self.foldEdit.setText(foldPath)

    def onClickStart(self):
        if self.foldPath is None:
            QMessageBox.information(self,"","设置图片目录",QMessageBox.Ok)
            return

        scaleStr = self.scaleEdit.text()
        if scaleStr:
            self.scale = float(scaleStr)

        directNewPage = True
        if self.fillBox.isChecked():
            directNewPage = False

        autoScale = float(self.autoScaleEdit.text())

        exportPdfFile(self.foldPath,scale=self.scale,directNewPage=directNewPage,autoScale=autoScale)

        QMessageBox.information(self,"","导出成功",QMessageBox.Ok)


