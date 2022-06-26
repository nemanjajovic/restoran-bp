from styles import *
from helper_widgets import *
from PySide6.QtWidgets import *
from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon
#from db import Connection
from forms import *

class MenuMainView(MainView):
    def __init__(self):
        super().__init__("Meni")
        #---------FORM-WINDOW-----------
        self.form = MenuForm()

        # ---------WIDGETS--------------
        self.search = QLineEdit()
        self.addItem = QPushButton("+ Add Item")
        self.butt1 = QPushButton("PICE")
        self.butt2 = QPushButton("HRANA")
        column_list = []

        # with Connection() as handler:
        #     columns = handler.get_column_names("Narudzbe")
        #     for column in columns:
        #         column_list.append(column[3])
        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(column_list)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        self.addItem.setStyleSheet(add)
        
        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.butt1, self.butt2, self.textBox)
        self.fill_rtop(self.search, self.addItem)
        self.fill_rlayout(self.table)

        self.butt1.clicked.connect(self.button_click)
        
        self.addItem.clicked.connect(self.form.show)

class ScheduleMainView(MainView):
    def __init__(self):
        super().__init__("Raspored")
        # this is just a placeholder
        columns = ["gasdgsad", "shdah", "ASF"]
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
        for i in range(30):
            self.buttons.append(QPushButton())
            self.buttons[i].setIcon(self.icon)
            self.buttons[i].setFixedSize(QSize(100,100))
            self.buttons[i].setIconSize(QSize(120,120))
            self.buttons[i].pressed.connect(lambda i=i+1: self.test(i))
            
        self.addButton = QPushButton("+ Reservation")
        self.filler = QLabel()
        self.calendar = QCalendarWidget()
        sliderLbl = SliderLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.freeLabel = IconLabel("assets/freeTable.png", "-  Slobodno")
        self.reservedLabel = IconLabel("assets/reservedTable.png", "-  Rezervisano")
        self.takenLabel = IconLabel("assets/takenTable.png", "-  Zauzeto")

        # ---------STYLES---------------
        self.filler.setStyleSheet("QLabel{max-width:40px}")
        self.calendar.setStyleSheet(cal)
        self.slider.setRange(0, 20) # 20 ticks
        self.rFrame.setObjectName(f"frame{1}")

        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.calendar,self.addButton, self.textBox,self.freeLabel, self.reservedLabel, self.takenLabel)
        self.fill_rtop(sliderLbl, self.slider)  
        self.fill_grid()

        self.addButton.clicked.connect(self.addForm.show)

    def test(self, number):
        print(number)

    def fill_grid(self):
        self.rlayout.addWidget(self.rFrame)
        self.rlayout.setContentsMargins(0, 0, 0, 0)
        x = 0
        for i in range(6):
            for j in range(5):
                # skip showing these tables
                if x in [3,8,10,11,12,13,16,18,21,23,28]:
                    x += 1
                    continue
                self.rFrame.layout.addWidget(self.buttons[x],i,j)
                x += 1
        self.rFrame.layout.addWidget(self.filler,0,3)


class ReceiptMainView(MainView):
    def __init__(self):
        super().__init__("Racuni")
        # this is just a placeholder
        columns = ["gasdgsad", "shdah", "ASF"]
    
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
        super().__init__("Radnici")
        # this is just a placeholder
        columns = ["gasdgsad", "shdah", "ASF"]

        self.workerForm = WorkerAddForm()

        # ---------WIDGETS--------------
        b1 = QPushButton("Svi")
        b2 = QPushButton("Servis")
        b3 = QPushButton("Kuhinja")
        b4 = QPushButton("Pomocni")
        self.addWorkerButton = QPushButton("+ Novi Radnik")
        self.search = QLineEdit()

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        self.addWorkerButton.setStyleSheet(add)

        # --------FILL-LAYOUTS----------
        self.fill_llayout(b1,b2,b3,b4, self.textBox)
        self.fill_rtop(self.search, self.addWorkerButton)
        self.fill_rlayout(self.table)

        self.addWorkerButton.clicked.connect(self.workerForm.show)