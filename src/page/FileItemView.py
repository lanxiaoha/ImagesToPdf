from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from .ui.MergeFileItemView import Ui_Form as FileItemUI
from .datas import FileItemData
from .FileItemSettingsDialog import FileItemSettingsDialog


class FileWidgetItem(QListWidgetItem):
    filename: str = ""
    position: int = 0

    def __init__(self, itemData: FileItemData, onClickMoveUpListener=None, onClickMoveDownListener=None):
        super().__init__()
        self.itemData = itemData
        self.onClickMoveUpListener = onClickMoveUpListener
        self.onClickMoveDownListener = onClickMoveDownListener
        self.onClickDeleteListener = None

        self.fileItemView = FileItemView(itemData)
        self.widget = self.fileItemView
        self.setSizeHint(QSize(0, 50))
        self.fileItemView.upBtnView.clicked.connect(self.onClickMoveUp)
        self.fileItemView.downBtnView.clicked.connect(self.onClickMoveDown)
        self.fileItemView.moreBtnView.clicked.connect(self.showSettingsDialog)

    def onClickMoveUp(self):
        print("xxx")
        if self.onClickMoveUpListener is not None:
            self.onClickMoveUpListener(self.itemData)

    def onClickMoveDown(self):
        if self.onClickMoveDownListener is not None:
            self.onClickMoveDownListener(self.itemData)

    def showSettingsDialog(self):

        dialog = FileItemSettingsDialog(self.itemData)
        dialog.onClickDeleteListener = self._onClickDeleteListener
        dialog.onClickSplitListener = self._onClickSplitListener
        dialog.exec()

    def _onClickDeleteListener(self, itemData):
        if self.onClickDeleteListener is not None:
            self.onClickDeleteListener(itemData)

    def _onClickSplitListener(self, itemData: FileItemData, startPos: int, endPos: int):
        itemData.startPos = startPos
        itemData.endPos = endPos
        print("设置裁剪位置", str(startPos), str(endPos))


class FileItemView(QWidget, FileItemUI):
    """
    https://juejin.cn/s/pyqt%20qlistwidget%E8%87%AA%E5%AE%9A%E4%B9%89item

    https://blog.csdn.net/Strengthennn/article/details/103747819
    """
    filename: str = ""
    position: int = 0

    def __init__(self, itemData: FileItemData):
        super().__init__()
        self.setupUi(self)
        # self.fileNameLabelView.setText(filename)
        self.fileNameLabelView.setText(itemData.filePath)
