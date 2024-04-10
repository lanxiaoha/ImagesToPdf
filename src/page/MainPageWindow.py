from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox

from .ui.MergePdfWindow import Ui_MainPage
from .FileItemView import FileItemView, FileWidgetItem
from .datas import FileItemData
from .PdfOperate import mergeFDF
import os.path


class MainPageWindow(QMainWindow, Ui_MainPage):
    pdfFilenameList: list[FileItemData] = []

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("合并PDF")
        self.setFixedSize(self.width(), self.height())
        self.initListener()
        self.savePathDir: str = ""

    def initListener(self):
        self.addBtnView.clicked.connect(self.onClickAddFile)
        self.setSavePathBtnView.clicked.connect(self.onClickSetSavePath)
        self.exportBtnView.clicked.connect(self.exportPdf)

    def onClickAddFile(self):
        home_dir = str(Path.home())
        dialog: QFileDialog = QFileDialog()
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setNameFilter("PDF (*.pdf)")
        if dialog.exec():
            filename = dialog.selectedFiles()
            if filename:
                self.onNewFileAdd(filename[0])

    def onNewFileAdd(self, filename):
        itemData = FileItemData(filePath=filename)
        self.pdfFilenameList.append(itemData)
        position = len(self.pdfFilenameList) - 1
        self.addListViewItem(itemData)

    def addListViewItem(self, itemData: FileItemData):
        itemView = self.createListViewItemView(itemData)
        self.listView.addItem(itemView)
        self.listView.setItemWidget(itemView, itemView.widget)

    def createListViewItemView(self, itemData: FileItemData):
        itemView = FileWidgetItem(itemData,
                                  onClickMoveUpListener=self._onClickMoveUpListener,
                                  onClickMoveDownListener=self._onClickMoveDownListener)
        itemView.onClickDeleteListener = self._onClickDeleteListener
        return itemView

    def _onClickDeleteListener(self, itemData: FileItemData):
        position = self.pdfFilenameList.index(itemData)
        if position < 0:
            return

        self.pdfFilenameList.pop(position)
        item = self.listView.takeItem(position)
        self.listView.removeItemWidget(item)

    def _onClickMoveDownListener(self, itemData: FileItemData):
        print("_onClickMoveDownListener", str(itemData.filePath))

        position = self.pdfFilenameList.index(itemData)

        if position >= len(self.pdfFilenameList) - 1:
            return

        item = self.listView.takeItem(position)
        self.listView.removeItemWidget(item)

        value = self.pdfFilenameList.pop(position)
        self.pdfFilenameList.insert(position + 1, value)

        if item:
            self.listView.clearSelection()
            newItem = self.createListViewItemView(itemData)
            self.listView.insertItem(position + 1, newItem)
            self.listView.setItemWidget(newItem, newItem.fileItemView)

    def _onClickMoveUpListener(self, itemData: FileItemData):
        print("_onClickMoveUpListener", str(itemData.filePath))

        position = self.pdfFilenameList.index(itemData)

        if position <= 0:
            return

        item = self.listView.takeItem(position)
        self.listView.removeItemWidget(item)

        value = self.pdfFilenameList.pop(position)
        self.pdfFilenameList.insert(position - 1, value)

        if item:
            self.listView.clearSelection()
            newItem = self.createListViewItemView(itemData)
            self.listView.insertItem(position - 1, newItem)
            self.listView.setItemWidget(newItem, newItem.fileItemView)

    def onClickSetSavePath(self):
        dialog: QFileDialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.DirectoryOnly)
        if dialog.exec():
            dirs = dialog.selectedFiles()
            if dirs:
                dir = dirs[0]
                self.savePathDir = dir
                self.savePathTextView.setText(dir)

    def exportPdf(self):

        if len(self.savePathDir) == 0:
            QMessageBox.information(self, "提示", '先设置保存路径', QMessageBox.Ok)
            return

        if len(self.pdfFilenameList) < 1:
            QMessageBox.information(self, "提示", '至少要两个PDF', QMessageBox.Ok)
            return

        saveFileNamePrefix = "result_merge"
        saveFileName = saveFileNamePrefix + ".pdf"
        count = 1000
        index = 0
        while index < count:
            filePath = os.path.join(self.savePathDir, saveFileName)
            if os.path.exists(filePath):
                saveFileName = saveFileNamePrefix + "_" + str(index) + ".pdf"
                index = index + 1
            else:
                break

        savePath = os.path.join(self.savePathDir, saveFileName)

        result = False
        try:
            result = mergeFDF(savePath, self.pdfFilenameList)
        except:
            QMessageBox.information(self, "提示", '导出失败', QMessageBox.Ok)
            return
        else:
            if result:
                QMessageBox.information(self, "提示", '导出成功', QMessageBox.Ok)
            else:
                QMessageBox.information(self, "提示", '导出失败', QMessageBox.Ok)
