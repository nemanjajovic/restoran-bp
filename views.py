import pandas as pd
from styles import *
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel
from PySide6.QtWidgets import *
from PySide6 import QtWidgets

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

class MenuMainView():
    def __init__(self):
        columns = ["gasdgsad", "shdah", "ASF"]
        # ---------LAYOUTS--------------
        self.llayout = QVBoxLayout()
        self.rlayout = QVBoxLayout()
        self.rtop    = QHBoxLayout()

        self.rlayout.addLayout(self.rtop)
        self.rtop.setAlignment(Qt.AlignLeft)

        # ---------WIDGETS--------------
        self.label = QLabel()
        self.search = QLineEdit()
        self.addItem = QPushButton("+ Add Item")
        self.butt1 = QPushButton("PICE")
        self.butt2 = QPushButton("HRANA")

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.label.setStyleSheet(qss1)
        self.search.setStyleSheet(search)
        self.addItem.setStyleSheet(add)
        self.butt1.setStyleSheet(menu)
        self.butt2.setStyleSheet(menu)

        self.butt1.setFlat(True)
        self.butt2.setFlat(True)
        
        # --------ADD-LEFT-WIDGETS ----------
        self.llayout.addWidget(self.butt1)
        self.llayout.addWidget(self.butt2)
        self.llayout.addWidget(self.label)

        # --------ADD-RIGHT-WIDGETS ----------
        self.rtop.addWidget(self.search)
        self.rtop.addWidget(self.addItem)
        self.rlayout.addWidget(self.table)

class ReservationMainView():
    def __init__(self):
        # ---------LAYOUTS--------------
        self.llayout = QVBoxLayout()
        self.rlayout = QVBoxLayout()

        # ---------WIDGETS--------------
        self.add = QPushButton("+ Reservation")
        self.tlocrt = QLabel("Tlocrt")
        self.calendar = QCalendarWidget()
        self.slider = QSlider(Qt.Horizontal)
        self.labels = QLabel("""
                - Free
                - Taken
                - Reserved""")

        # ---------STYLES---------------
        self.tlocrt.setStyleSheet(tlo)
        self.calendar.setStyleSheet(cal)
        self.labels.setAlignment(Qt.AlignBottom)
        self.llayout.setAlignment(Qt.AlignTop)

        # -----ADD-LEFT-WIDGETS --------
        self.llayout.addWidget(self.add)
        self.llayout.addWidget(self.calendar)
        self.llayout.addWidget(self.labels)

        # ----ADD-RIGHT-WIDGETS --------
        self.rlayout.addWidget(self.slider)
        self.rlayout.addWidget(self.tlocrt)

class ReceiptMainView():
    def __init__(self):
        columns = ["gasdgsad", "shdah", "ASF"]
        # ---------LAYOUTS--------------
        self.llayout = QVBoxLayout()
        self.rlayout = QVBoxLayout()
        self.rtop    = QHBoxLayout()

        self.rlayout.addLayout(self.rtop)

        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.search = QLineEdit()

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)
        self.search.setStyleSheet(search)
        self.llayout.setAlignment(Qt.AlignTop)
        self.rtop.setAlignment(Qt.AlignLeft)

        # -----ADD-LEFT-WIDGETS --------
        self.llayout.addWidget(self.calendar)

        # ----ADD-RIGHT-WIDGETS --------
        self.rtop.addWidget(self.search)
        self.rlayout.addWidget(self.table)