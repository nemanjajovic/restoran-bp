from PySide6.QtWidgets import *
from PySide6 import QtWidgets
from styles import *
from db import Connection
from helper_widgets import MainForm

class MenuForm(MainForm):
    """ A form window for the menu table."""
    def __init__(self):
        super().__init__()
        # ---------WIDGETS---------
        self.name = QLineEdit()
        self.type = QLineEdit()
        self.category = QLineEdit()
        self.price = QLineEdit()
        self.button = QPushButton("Confirm")

        # labels
        lnames = ["Naziv: ", "Tip: ", "Kategorija: ", "Cijena: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)

        # ---------LAYOUT---------
        self.layout.addWidget(self.name, 0, 1)
        self.layout.addWidget(self.type, 1, 1)
        self.layout.addWidget(self.category, 2, 1)
        self.layout.addWidget(self.price, 3, 1)
        self.layout.addWidget(self.button, 4, 1)

        # ----------STYLES---------
        self.setStyleSheet("QPushButton{max-width:100px;margin-left:150px;}QLineEdit{max-width:300px;margin-right:50px;}QLabel{font-size:20px;margin-left:50px;}")
        self.setFixedSize(500,340)


class ScheduleAddForm(MainForm):
    """ A form window for the schedule table."""
    def __init__(self):
        super().__init__()
        # ---------WIDGETS---------
        self.date = QLineEdit()
        self.worker = QLineEdit()
        self.shift = QLineEdit()
        self.position = QLineEdit()
        self.button = QPushButton("Confirm")

        # labels
        lnames = ["Datum: ", "Radnik: ", "Pocetak Smjene: ", "Pozicija: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)
        
        # ---------LAYOUT---------
        self.layout.addWidget(self.date, 0, 1)
        self.layout.addWidget(self.worker, 1, 1)
        self.layout.addWidget(self.shift, 2, 1)
        self.layout.addWidget(self.position, 3, 1)
        self.layout.addWidget(self.button, 4, 1)

        # ----------STYLES---------
        self.setStyleSheet("QPushButton{max-width:100px;margin-left:150px;}QLineEdit{max-width:300px;margin-right:50px;}QLabel{font-size:20px;margin-left:20px;}")
        self.setFixedSize(500,340)

class ScheduleWeekForm(MainForm):
    def __init__(self):
        super().__init__()

class ReservationAddForm(MainForm):
    """ A form window for the reservations table."""
    def __init__(self):
        super().__init__()
        # ---------WIDGETS---------
        self.nr_of_guests = QLineEdit()
        self.time   = QLineEdit()
        self.table  = QLineEdit()
        self.name   = QLineEdit()
        self.contact= QLineEdit()
        self.remark = QLineEdit()
        self.button = QPushButton("Confirm")

        # labels
        lnames = ["Broj Gostiju: ", "Vrijeme: ", "Stol: ", "Naziv: ", "Kontakt: ", "Napomena: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)

        # ---------LAYOUT---------
        self.layout.addWidget(self.nr_of_guests, 0, 1)
        self.layout.addWidget(self.time, 1, 1)
        self.layout.addWidget(self.table, 2, 1)
        self.layout.addWidget(self.name, 3, 1)
        self.layout.addWidget(self.contact, 4, 1)
        self.layout.addWidget(self.remark, 5, 1)
        self.layout.addWidget(self.button, 6, 1)

        # ----------STYLES---------
        self.setStyleSheet("QPushButton{max-width:100px;margin-left:150px;}QLineEdit{max-width:300px;margin-right:50px;}QLabel{font-size:20px;margin-left:50px;}")
        self.setFixedSize(500,340)

class WorkerAddForm(MainForm):
    """ A form window for the workers table."""
    def __init__(self):
        super().__init__()
        # ----------WIDGETS----------
        self.name   = QLineEdit()
        self.type= QLineEdit()
        self.button = QPushButton("Confirm")

        # labels
        lnames = ["Naziv: ", "Tip (servis ili kuhinja): "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)

        # ----------LAYOUT----------
        self.layout.addWidget(self.name, 0, 1)
        self.layout.addWidget(self.type, 1, 1)
        self.layout.addWidget(self.button, 2, 1)

        # ----------STYLES---------
        self.setStyleSheet("QPushButton{max-width:100px;margin-left:100px;}QLineEdit{max-width:300px;margin-right:30px;}QLabel{font-size:20px;margin-left:20px;}")
        self.setFixedSize(500,340)

        self.button.clicked.connect(self.confirm)

    def confirm(self):
        values = f"'{self.name.text()}','{self.type.text()}','00:00:00'"
        with Connection() as handler:
            handler.insert("Radnici", "radnik_naziv,radnik_tip,radnik_sati", values)