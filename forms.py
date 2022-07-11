from PySide6.QtWidgets import *
from PySide6 import QtWidgets
from styles import *
from db import Connection
from helper_widgets import MainForm, get_column_string
from data import itemCategories, workerCategories

class MenuForm(MainForm):
    """ A form window for the menu table."""
    def __init__(self, tableName, columns, frame, textBox):
        super().__init__(tableName, columns, textBox)
        self.lastClicked = ""
        
        # ---------WIDGETS---------
        self.name = QLineEdit()
        self.typeBox = QComboBox()
        self.catBox = QComboBox()
        self.category = QLineEdit()
        self.price = QLineEdit()
        self.button = QPushButton("Confirm")
        self.rFrame = frame

        # labels
        lnames = ["Naziv: ", "Tip: ", "Kategorija: ", "Cijena: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)

        # ----FILL-COMBOBOX-----
        self.typeBox.addItem("Pice")
        self.typeBox.addItem("Hrana")
        self.catBox.addItems(itemCategories[0])


        # ---------LAYOUT---------
        self.layout.addWidget(self.name, 0, 1)
        self.layout.addWidget(self.typeBox, 1, 1)
        self.layout.addWidget(self.catBox, 2, 1)
        self.layout.addWidget(self.price, 3, 1)
        self.layout.addWidget(self.button, 4, 1)

        # ----------STYLES---------
        self.setStyleSheet("QPushButton{max-width:100px;margin-left:150px;}QLineEdit{max-width:300px;margin-right:50px;}QLabel{font-size:20px;margin-left:50px;}QComboBox{max-width:257px;}")
        self.setFixedSize(500,340)

        # ---------CONNECTIONS----------
        self.button.pressed.connect(lambda: self.confirm(columns))
        self.typeBox.currentIndexChanged.connect(self.update_combobox)

    def confirm(self,columns):     
        values = f"'{self.name.text()}','{self.typeBox.currentText()}','{self.catBox.text()}','{self.price.text()}'"
        self.insert(columns, values)
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, "")
        self.replace_table(rows, column_list, "")
        self.update_textbox(query)

    def update_combobox(self, index):
        self.catBox.clear()
        self.catBox.addItems(itemCategories[index])

    def search(self, text):
        cond = f"artikal_naziv LIKE '{text}%' {self.lastClicked}" if text else ""
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, cond)
        self.replace_table(rows, column_list, cond)
        self.update_textbox(query)

    def show_table(self, cond):
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, cond)
        self.replace_table(rows, column_list, cond)
        self.update_textbox(query)
        self.lastClicked = f"AND {cond}"

class ScheduleForm(MainForm):
    """ A form window for the schedule table."""
    def __init__(self, table, columns, calendar, frame, textBox):
        super().__init__(table, columns, textBox)
        self.rFrame = frame
        _date = calendar.selectedDate().toString("dd-MM-yyyy")
        self.date = calendar.selectedDate().toString("MM/dd/yyyy")
        self.workers = self.available_workers()
        self.ids = [row[0] for row in self.workers]

        # ---------WIDGETS---------
        ldateLabel = QLabel("Datum: ")
        rdateLabel = QLabel(_date)
        button = QPushButton("Confirm")

        # labels
        lnames = [ "Radnik: ", "Pocetak Smjene: ", "Pozicija: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i+1, 0)

        # -------COMBOBOXES--------
        self.workerBox = QComboBox()
        for row in self.workers:
            # name + ' ' + surname
            self.workerBox.addItem(row[1]+' '+ row[2]) 

        self.typeBox = QComboBox()
        for elem in ["Servis", "Kuhinja", "Pomocni"]:
            self.typeBox.addItem(elem)

        self.timeBox = QComboBox()
        for time in ['09:00', '10:00', '11:00', '12:00', '13:00']:
            self.timeBox.addItem(time)
        
        # ---------LAYOUT---------
        self.layout.addWidget(ldateLabel, 0, 0)
        self.layout.addWidget(rdateLabel, 0, 1)
        self.layout.addWidget(self.workerBox, 1, 1)
        self.layout.addWidget(self.timeBox, 2, 1)
        self.layout.addWidget(self.typeBox, 3, 1)
        self.layout.addWidget(button, 4, 1)

        # ----------STYLES---------
        ldateLabel.setAlignment(Qt.AlignRight)
        self.setStyleSheet("QPushButton{max-width:100px;margin-left:150px;}QLineEdit{max-width:300px;margin-right:50px;}QLabel{font-size:20px;margin-left:20px;max-height:30px;}")
        self.setFixedSize(500,340)

        button.clicked.connect(lambda: self.confirm(columns))

    def available_workers(self):
        rows = []
        _query = f"""SELECT rd.radnik_id,rd.radnik_ime,rd.radnik_prezime FROM Radnici rd LEFT JOIN Raspored ON rd.radnik_id= Raspored.radnik_id WHERE Raspored.radnik_id IS NULL"""
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            for row in handler.cursor.execute(_query):
                rows.append(row)
        self.update_textbox(_query)
        return rows

    def confirm(self, columns):
        _id = self.get_selected_id()   
        values = f"'{_id}','{self.date}','{self.timeBox.text()}','{self.typeBox.text()}'"
        column_list = self.insert_worker(columns, values)
        query, rows = handler.select("*", self.tableName, "")
        self.replace_table(rows, column_list, "")
        self.update_textbox(query)

    def insert_worker(self, columns, values):
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, _ = handler.insert(self.tableName, columns, values)
            self.update_textbox(query)
        return column_list

    def get_selected_id(self):
        # "ime prezime" -> ["ime", "prezime"]
        selected = self.workerBox.currentText().split()
        for worker in self.workers:
            # worker is tuple, ex. (3, "ime", "prezime")
            if selected[0] in worker and selected[1] in worker:
                return row[0]

    def show_date(self, date):
        date = date.toString("yyyy-MM-dd")
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, f"raspored_datum='{date}'")
        self.replace_table(rows, column_list, "")
        self.update_textbox(query)
        

class ScheduleWeekForm(MainForm):
    def __init__(self):
        super().__init__()

class ReservationAddForm(MainForm):
    """ A form window for the reservations table."""
    def __init__(self, table, columns, textBox):
        super().__init__(table, columns, textBox)
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

class ReceiptForm(MainForm):
    
    def __init__(self, tableName, columns, frame, textBox):
        super().__init__(tableName, columns, textBox)
        self.rFrame = frame

    def show_date(self, date):
        date = date.toString("yyyy-MM-dd")
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, f"racun_datum='{date}' ORDER BY racun_vrijeme")
        self.replace_table(rows, column_list, "")
        self.update_textbox(query)

class WorkerForm(MainForm):
    """ A form window for the workers table."""

    def __init__(self, tableName, columns, frame, textBox):
        super().__init__(tableName, columns, textBox)
        self.tableName = tableName
        self.lastClicked = ""

        # ----------WIDGETS----------
        self.rFrame = frame
        self.name   = QLineEdit()
        self.surname= QLineEdit()
        self.button = QPushButton("Confirm")

        # ComboBox
        self.typeBox= QComboBox()
        for elem in ["Servis", "Kuhinja", "Pomocni"]:
            self.typeBox.addItem(elem)

        # labels
        lnames = ["Ime: ", "Prezime: ", "Tip: "]
        for i,text in enumerate(lnames):
            label = QLabel(text)
            label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label, i, 0)

        # ----------LAYOUT----------
        self.layout.addWidget(self.name, 0, 1)
        self.layout.addWidget(self.surname, 1, 1)
        self.layout.addWidget(self.typeBox, 2, 1)
        self.layout.addWidget(self.button, 3, 1)

        # ----------STYLES---------
        self.typeBox.setStyleSheet("QComboBox{max-width:300px;}")
        self.setStyleSheet("QPushButton{max-width:100px;margin-left:100px;}QLineEdit{max-width:300px;margin-right:30px;}QLabel{font-size:20px;margin-left:20px;}")
        self.setFixedSize(500,340)

        self.button.pressed.connect(lambda:self.confirm(columns))

    def confirm(self, columns):     
        values = f"'{self.name.text()}','{self.surname.text()}','00:00:00','{self.typeBox.currentText()}'"
        self.insert(columns, values)
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, "")
        self.replace_table(rows, column_list, "")
        self.update_textbox(query)

    def worker_show_all(self):
        self.lastClicked = ""
        self.show_all()

    def search(self, text):
        cond = f"(radnik_ime LIKE '{text}%' OR radnik_prezime LIKE '{text}%') {self.lastClicked}" if text else ""
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, cond)
        self.replace_table(rows, column_list, cond)
        self.update_textbox(query)

    def show_table(self, cond):
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, cond)
        self.replace_table(rows, column_list, cond)
        self.update_textbox(query)
        self.lastClicked = f"AND {cond}"