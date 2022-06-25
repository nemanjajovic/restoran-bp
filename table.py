import pandas as pd
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel

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

            #if orientation == Qt.Vertical:
             #   return str(self._data.index[section])

class IconLabel(QWidget):

    IconSize = QSize(24, 24)
    HorizontalSpacing = 2

    def __init__(self, icon_path, text, final_stretch=True):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        icon = QLabel()
        icon.setPixmap(QIcon(icon_path).pixmap(self.IconSize))

        layout.addWidget(QLabel("                                      "))      
        layout.addWidget(icon)
        #layout.addSpacing(self.HorizontalSpacing)
        layout.addWidget(QLabel(text))
        #layout.setAlignment(Qt.AlignRight)
        #icon.setStyleSheet("QLabel{max-width:16px'}")

        if final_stretch:
            layout.addStretch()

