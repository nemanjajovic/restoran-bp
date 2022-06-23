from PySide6.QtWidgets import *
from PySide6 import QtWidgets
from styles import *
from db import Connection

class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        centralWidget = QWidget()
        # ----------LAYOUT-----------
        self.layout = QGridLayout()
        centralWidget.setLayout(self.layout)
        # ----------STYLE------------
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Form")
        self.setFixedSize(640,320)
        self.setStyleSheet(qss)

        self.setCentralWidget(centralWidget)

    def insert(self, table, columns, values):
        with Connection() as handler:
            handler.insert(table, columns, values)

class MenuForm(MainForm):
    def __init__(self):
        super().__init__()

        self.name = QLineEdit()
        self.type = QLineEdit()
        self.category = QLineEdit()
        self.price = QLineEdit()
        self.button = QPushButton("Confirm")

        lnames = ["Naziv: ", "Tip: ", "Kategorija: ", "Cijena: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)

        self.layout.addWidget(self.name, 0, 1)
        self.layout.addWidget(self.type, 1, 1)
        self.layout.addWidget(self.category, 2, 1)
        self.layout.addWidget(self.price, 3, 1)
        self.layout.addWidget(self.button, 4, 1)

        self.setStyleSheet("QPushButton{max-width:100px;margin-left:150px;}QLineEdit{max-width:300px;margin-right:50px;}QLabel{font-size:20px;margin-left:50px;}")
        self.setFixedSize(500,340)

    def add(self):
        with Connection() as handler:
            pass

class ScheduleAddForm(MainForm):
    def __init__(self):
        super().__init__()

        self.date = QLineEdit()
        self.worker = QLineEdit()
        self.shift = QLineEdit()
        self.position = QLineEdit()
        self.button = QPushButton("Confirm")

        lnames = ["Datum: ", "Radnik: ", "Pocetak Smjene: ", "Pozicija: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)

        self.layout.addWidget(self.date, 0, 1)
        self.layout.addWidget(self.worker, 1, 1)
        self.layout.addWidget(self.shift, 2, 1)
        self.layout.addWidget(self.position, 3, 1)
        self.layout.addWidget(self.button, 4, 1)

        self.setStyleSheet("QPushButton{max-width:100px;margin-left:150px;}QLineEdit{max-width:300px;margin-right:50px;}QLabel{font-size:20px;margin-left:20px;}")
        self.setFixedSize(500,340)

class ScheduleWeekForm(MainForm):
    def __init__(self):
        super().__init__()

class ReservationAddForm(MainForm):
    def __init__(self):
        super().__init__()
        self.nr_of_guests = QLineEdit()
        self.time   = QLineEdit()
        self.table  = QLineEdit()
        self.name   = QLineEdit()
        self.contact= QLineEdit()
        self.remark = QLineEdit()
        self.button = QPushButton("Confirm")

        lnames = ["Broj Gostiju: ", "Vrijeme: ", "Stol: ", "Naziv: ", "Kontakt: ", "Napomena: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)

        self.layout.addWidget(self.nr_of_guests, 0, 1)
        self.layout.addWidget(self.time, 1, 1)
        self.layout.addWidget(self.table, 2, 1)
        self.layout.addWidget(self.name, 3, 1)
        self.layout.addWidget(self.contact, 4, 1)
        self.layout.addWidget(self.remark, 5, 1)
        self.layout.addWidget(self.button, 6, 1)

        self.setStyleSheet("QPushButton{max-width:100px;margin-left:150px;}QLineEdit{max-width:300px;margin-right:50px;}QLabel{font-size:20px;margin-left:50px;}")
        self.setFixedSize(500,340)