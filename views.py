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

class MainView(QtWidgets.QWidget):
    def __init__(self, viewName):
        super().__init__()
        self.layout = QHBoxLayout()

        self.llayout = QVBoxLayout()
        self.rlayout = QVBoxLayout()
        self.rtop    = QHBoxLayout()
        self.llayout.setContentsMargins(0, 0, 0, 0)

        self.rlayout.addLayout(self.rtop)
        self.layout.addLayout(self.llayout)
        self.layout.addLayout(self.rlayout)

        self.setLayout(self.layout)

        self.llayout.setAlignment(Qt.AlignTop)
        self.rtop.setAlignment(Qt.AlignLeft)

        # -----
        self.viewLabel = QLabel(viewName)
        self.viewLabel.setStyleSheet(naslov)

    def fill_llayout(self, widgets):
        self.llayout.addWidget(self.viewLabel)
        for widget in widgets:
            self.llayout.addWidget(widget)
    
    def fill_rlayout(self, widgets):
        for widget in widgets:
            self.rlayout.addWidget(widget)

class MenuMainView(MainView):
    def __init__(self):
        super().__init__("Meni")
        columns = ["gasdgsad", "shdah", "ASF"]
        # ---------WIDGETS--------------
        self.label = QLabel()
        self.search = QLineEdit()
        self.addItem = QPushButton("+ Add Item")
        self.butt1 = QPushButton("PICE")
        self.butt2 = QPushButton("HRANA")
        frame = ButtonFrame([self.butt1,self.butt2])

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.label.setStyleSheet(qss1)
        self.search.setStyleSheet(search)
        self.addItem.setStyleSheet(add)
        self.butt1.setStyleSheet(menu)
        self.butt2.setStyleSheet(menu)
        frame.setFixedHeight(60)

        self.butt1.setFlat(True)
        self.butt2.setFlat(True)
        
        # --------FILL-LEFT-WIDGETS ----------
        self.fill_llayout([frame, self.label])

        # --------ADD-RIGHT-WIDGETS ----------
        self.rtop.addWidget(self.search)
        self.rtop.addWidget(self.addItem)
        self.rlayout.addWidget(self.table)

class ScheduleMainView(MainView):
    def __init__(self):
        super().__init__("Raspored")
        columns = ["gasdgsad", "shdah", "ASF"]

        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.weekButton = QPushButton("Sedmicni Raspored")

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)

        # -----ADD-LEFT-WIDGETS --------
        self.fill_llayout([self.calendar, self.weekButton])

        # ----ADD-RIGHT-WIDGETS --------
        self.rlayout.addWidget(self.table)

class ReservationMainView(MainView):
    def __init__(self):
        super().__init__("Rezervacije")
        # ---------WIDGETS--------------
        self.addButton = QPushButton("+ Reservation")
        self.tlocrt = QLabel("Tlocrt")
        self.calendar = QCalendarWidget()
        sliderLbl = SliderLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.infoLabels = QLabel("""
                - Free
                - Taken
                - Reserved""")

        # ---------STYLES---------------
        self.tlocrt.setStyleSheet(tlo)
        self.calendar.setStyleSheet(cal)
        self.infoLabels.setAlignment(Qt.AlignBottom)
        self.slider.setRange(0, 20)

        # -----ADD-LEFT-WIDGETS --------
        self.fill_llayout([self.addButton,self.calendar,self.infoLabels])

        # ----ADD-RIGHT-WIDGETS --------
        self.fill_rlayout([
            sliderLbl,
            self.slider,
            self.tlocrt,
            ])              

class ReceiptMainView(MainView):
    def __init__(self):
        super().__init__("Racuni")
        columns = ["gasdgsad", "shdah", "ASF"]

        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.search = QLineEdit()

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)
        self.search.setStyleSheet(search)

        # -----ADD-LEFT-WIDGETS --------
        self.fill_llayout([self.calendar])

        # ----ADD-RIGHT-WIDGETS --------
        self.rtop.addWidget(self.search)
        self.rlayout.addWidget(self.table)

class WorkersMainView(MainView):
    def __init__(self):
        super().__init__("Radnici")
        columns = ["gasdgsad", "shdah", "ASF"]

        # ---------WIDGETS--------------
        b1 = QPushButton("Svi")
        b2 = QPushButton("Servis")
        b3 = QPushButton("Kuhinja")
        b4 = QPushButton("Pomocni")
        buttonFrame = ButtonFrame([b1,b2,b3,b4])        
        self.search = QLineEdit()

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)

        # -----ADD-LEFT-WIDGETS --------
        self.fill_llayout([buttonFrame])

        # ----ADD-RIGHT-WIDGETS --------
        self.rtop.addWidget(self.search)
        self.rlayout.addWidget(self.table)

        b1.clicked.connect(lambda:self.test(b1.text()))
    
    def test(self, name):
        print(name)

class ButtonFrame(QtWidgets.QFrame):
    def __init__(self, buttons):
        super().__init__()
        but = QPushButton("")
        but.setFlat(True)
        but.setEnabled(False)
        vbox = QtWidgets.QVBoxLayout(self)
    
        self.setLayout(vbox)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedWidth(200)
        for button in buttons:
            vbox.addWidget(button)

class SliderLabel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setAlignment(Qt.AlignJustify)
        labels = [QLabel(str(i)) for i in range(1,13)]
        for label in labels:
            label.setFixedWidth(30)
            hbox.addWidget(label)