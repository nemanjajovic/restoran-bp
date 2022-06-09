import pandas as pd
from styles import *
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel
from PySide6.QtWidgets import *
from PySide6 import QtWidgets

class TableModel(QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._data = pd.DataFrame(
            [],
            columns=["gasd", "test", "ashd"],
            index=["Pygdssdg", "Row 2", "Row 3", "Row 4", "Row 5"],
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
        self.tableWidget = TableModel()
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
        # ---------LAYOUTS--------------
        self.llayout = QVBoxLayout()
        self.rlayout = QVBoxLayout()

        # ---------WIDGETS--------------
        self.tlocrt = QLabel("Racuni")
        self.calendar = QCalendarWidget()
        self.search = QLineEdit()


        # ---------STYLES---------------
        self.tlocrt.setStyleSheet(tlo)
        self.calendar.setStyleSheet(cal)
        self.search.setStyleSheet("max-width:250px;")
        self.llayout.setAlignment(Qt.AlignTop)

        # -----ADD-LEFT-WIDGETS --------
        self.llayout.addWidget(self.calendar)

        # ----ADD-RIGHT-WIDGETS --------
        self.rlayout.addWidget(self.search)
        self.rlayout.addWidget(self.tlocrt)