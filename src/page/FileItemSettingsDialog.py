from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog
from .ui.MergeFileSettingsDialog import Ui_Dialog as MergeFileSettingsDialog
from .datas import FileItemData


class FileItemSettingsDialog(QDialog, MergeFileSettingsDialog):

    def __init__(self, itemData: FileItemData):
        self.onClickDeleteListener = None
        self.onClickSplitListener = None
        self.itemData = itemData
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("")
        self.setFixedSize(430, 310)
        self.startPosEditView.setValidator(QIntValidator())
        self.endPosEditView.setValidator(QIntValidator())
        self.deleteBtnView.clicked.connect(self.onClickDelete)
        self.splitBtnView.clicked.connect(self.onClickSetSplit)

    def onClickDelete(self):
        if self.onClickDeleteListener is not None:
            self.onClickDeleteListener(self.itemData)

        self.close()

    def onClickSetSplit(self):

        startPos = None
        endPos = None

        startPosStr = self.startPosEditView.text()
        if startPosStr:
            startPos = int(startPosStr)

        endPosStr = self.endPosEditView.text()

        if endPosStr:
            endPos = int(endPosStr)

        if self.onClickSplitListener is not None:
            self.onClickSplitListener(self.itemData, startPos, endPos)
            self.close()
