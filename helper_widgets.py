import pandas as pd
from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel
from PySide6.QtGui import QPixmap, QIcon

class TableModel(QAbstractTableModel):
    def __init__(self, col=[], rows=[]):
        super().__init__()
        self._data = pd.DataFrame(
            [],
            columns = col,
            index = rows,
        )

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class IconLabel(QWidget):
    """A class combining an icon and text."""
    def __init__(self, icon_path, text, final_stretch=True):
        super().__init__()
        IconSize = QSize(24, 24)
        HorizontalSpacing = 2

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        icon = QLabel()
        icon.setPixmap(QIcon(icon_path).pixmap(IconSize))

        layout.addWidget(QLabel("                                      "))      
        layout.addWidget(icon)
        layout.addWidget(QLabel(text))

        if final_stretch:
            layout.addStretch()

