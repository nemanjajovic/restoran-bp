from styles import *
from helper_widgets import *
from PySide6.QtWidgets import *
from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon
from db import Connection
from forms import *

class MenuMainView(MainView):
    def __init__(self):
        # column names
        with Connection() as handler:
            columns = handler.get_column_names("MeniArtikli")

        super().__init__("Meni")
        #---------FORM-WINDOW-----------
        self.form = MenuForm()

        # ---------WIDGETS--------------
        self.search = QLineEdit()
        self.addItem = QPushButton("+ Add Item")
        self.butt1 = QPushButton("PICE")
        self.butt2 = QPushButton("HRANA")

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)
        header = self.table.horizontalHeader()

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        self.addItem.setStyleSheet(add)
        for i in range(len(columns)):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        
        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.butt1, self.butt2, self.textBox)
        self.fill_rtop(self.search, self.addItem)
        self.fill_rlayout(self.table)

        self.butt1.clicked.connect(self.button_click)
        
        self.addItem.clicked.connect(self.form.show)

class ScheduleMainView(MainView):
    def __init__(self):
        with Connection() as handler:
            columns = handler.get_column_names("Raspored")
        super().__init__("Raspored")
        self.addForm = ScheduleAddForm()

        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.addButton = QPushButton("Edit Raspored")
        self.weekButton = QPushButton("Pregled Sedmice")

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)

        # --------FILL-LAYOUTS----------  
        self.fill_llayout(self.calendar, self.addButton, self.weekButton, self.textBox)
        self.fill_rlayout(self.table)

        self.addButton.clicked.connect(self.addForm.show)

class ReservationMainView(MainView):
    placed = [0,]
    def __init__(self):
        super().__init__("Rezervacije")
        # override default (horizontal) MainView layout
        self.tFrame = MyFrame(QVBoxLayout)
        self.tFrame.setObjectName("frame2")
        self.addForm = ReservationAddForm()
        
        self.rFrame = MyFrame(QGridLayout)

        # ---------WIDGETS--------------
        self.icon= QIcon("assets/freeTable.png")
        self.buttons = []
        for i in range(20):
            self.buttons.append(QPushButton())
            butt = self.buttons[i]
            butt.setIcon(self.icon)
            butt.setFixedSize(QSize(100,100))
            butt.setIconSize(QSize(120,120))
            butt.pressed.connect(lambda i=i+1: self.test(i))
            
        self.addButton = QPushButton("+ Reservation")
        self.filler = QLabel()
        self.calendar = QCalendarWidget()
        sliderLbl = SliderLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.freeLabel = IconLabel("assets/freeTable.png", "-  Slobodno")
        self.reservedLabel = IconLabel("assets/reservedTable.png", "-  Rezervisano")
        self.takenLabel = IconLabel("assets/takenTable.png", "-  Zauzeto")

        # ---------STYLES---------------
        self.filler.setStyleSheet("QLabel{max-width:40px;max-height:40px;}")
        self.calendar.setStyleSheet(cal)
        self.slider.setRange(0, 10) # 20 ticks
        self.rFrame.setObjectName(f"frame{1}")

        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.calendar,self.addButton, self.textBox,self.freeLabel, self.reservedLabel, self.takenLabel)
        self.fill_rtop(sliderLbl, self.slider)  
        self.rlayout.addWidget(self.rFrame)
        self.rlayout.setContentsMargins(0, 0, 0, 0)
        self.fill_grid()

        self.addButton.clicked.connect(self.addForm.show)

    def test(self, number):
        self.tableForm = TableForm()
        self.tableForm.name_label.setText(str(number))
        self.tableForm.show()

    def fill_grid(self):
        index = 0
        for i in range(5):
            for j in range(6):
                button = self.buttons[index]
                # skip 2nd column and 3rd row
                if i == 2 or j == 3:
                    continue
                button.pressed.connect(lambda i=index+1: self.test(i))
                self.rFrame.layout.addWidget(button,i,j)
                index += 1
        self.buttons[5].setIcon(QIcon("assets/reservedTable.png"))
        self.rFrame.layout.addWidget(self.filler, 2, 3)

class ReceiptMainView(MainView):
    def __init__(self):
        with Connection() as handler:
            columns = handler.get_column_names("Racuni")
        super().__init__("Racuni")
        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.search = QLineEdit()
        self.button = QPushButton("Simuliraj Narudzbe")

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)
        self.search.setStyleSheet(search)

        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.calendar, self.button, self.textBox)
        self.fill_rtop(self.search)
        self.fill_rlayout(self.table)
    
class WorkersMainView(MainView):
    def __init__(self):
        with Connection() as handler:
            columns = handler.get_column_names("Radnici")
            
        super().__init__("Radnici")
        self.workerForm = WorkerAddForm()

        # ---------WIDGETS--------------
        self.buttons = [QPushButton(label) for label in ["Svi","Servis","Kuhinja","Pomocni"]]
        self.addWorkerButton = QPushButton("+ Novi Radnik")
        self.search = QLineEdit()

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        self.addWorkerButton.setStyleSheet("QPushButton{max-width:120px;}")

        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.buttons[0],self.buttons[1],self.buttons[2],self.buttons[3], self.textBox)
        self.fill_rtop(self.search, self.addWorkerButton)
        self.fill_rlayout(self.table)

        # --------BUTTON-ACTIONS--------
        self.addWorkerButton.clicked.connect(self.workerForm.show)