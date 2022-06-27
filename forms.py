from PySide6.QtWidgets import *
from PySide6 import QtWidgets
from styles import *

from helper_widgets import MainForm

class MenuForm(MainForm):
    """ A form window for the menu table."""
    def __init__(self, table, columns):
        super().__init__(table, columns)
        # ---------WIDGETS---------
        self.name = QLineEdit()
        self.type = QComboBox()
        self.category = QLineEdit()
        self.price = QLineEdit()
        self.button = QPushButton("Confirm")

        self.type.addItem("Pice")
        self.type.addItem("Hrana")

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
        self.type.setStyleSheet("QComboBox{max-width:257px;}")
        self.setStyleSheet("QPushButton{max-width:100px;margin-left:150px;}QLineEdit{max-width:300px;margin-right:50px;}QLabel{font-size:20px;margin-left:50px;}")
        self.setFixedSize(500,340)

        self.button.pressed.connect(lambda: self.confirm(table, columns))

    def confirm(self,table,columns):     
        values = f"'{self.name.text()}','{self.type.currentText()}','{self.category.text()}','{self.price.text()}'"
        self.insert(table, columns, values)

class ScheduleAddForm(MainForm):
    """ A form window for the schedule table."""
    def __init__(self, table, columns):
        super().__init__(table, columns)
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
    def __init__(self, table, columns):
        super().__init__(table, columns)
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
        
    def confirm(self):
        values = f"'{self.name.text()}','{self.type.text()}','00:00:00'"
        with Connection() as handler:
            handler.insert("Radnici", "radnik_naziv,radnik_tip,radnik_sati", values)    

class WorkerAddForm(MainForm):
    """ A form window for the workers table."""
    tipovi = ["Servis", "Kuhinja", "Pomocni"]
    def __init__(self, table, columns):
        super().__init__(table, columns)
        # ----------WIDGETS----------
        self.name   = QLineEdit()
        self.surname= QLineEdit()
        self.button = QPushButton("Confirm")

        # ComboBox
        self.type= QComboBox()
        for elem in self.tipovi:
            self.type.addItem(elem)

        # labels
        lnames = ["Ime: ", "Prezime: ", "Tip: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)

        # ----------LAYOUT----------
        self.layout.addWidget(self.name, 0, 1)
        self.layout.addWidget(self.surname, 1, 1)
        self.layout.addWidget(self.type, 2, 1)
        self.layout.addWidget(self.button, 3, 1)

        # ----------STYLES---------
        self.type.setStyleSheet("QComboBox{max-width:300px;}")
        self.setStyleSheet("QPushButton{max-width:100px;margin-left:100px;}QLineEdit{max-width:300px;margin-right:30px;}QLabel{font-size:20px;margin-left:20px;}")
        self.setFixedSize(500,340)

        self.button.pressed.connect(lambda:self.confirm(table,columns))

    def confirm(self,table,columns):     
        values = f"'{self.name.text()}','{self.surname.text()}','00:00:00','{self.type.currentText()}'"
        self.insert(table, columns, values)

class TableForm(MainForm):
    """ A form window for the individual restaurant tables."""
    def __init__(self):
        super().__init__()

        label = QLabel("")
        label.setAlignment(Qt.AlignRight)
        label.setStyleSheet("QLabel{font-size:30px}")
        self.layout.addWidget(label, 0, 0)

        self.name_label = QLabel()
        self.layout.addWidget(self.name_label, 0, 1)
        self.name_label.setStyleSheet("QLabel{font-size:30px}")
        self.setFixedSize(500,340)
