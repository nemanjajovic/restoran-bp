from styles import *
from helper_widgets import *
from PySide6.QtWidgets import *
from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon
from db import Connection
from forms import *

class MenuMainView(MainView):
    def __init__(self, tableName):
        super().__init__(tableName)
        # ---------WIDGETS--------------
        self.search = QLineEdit()
        self.addItem = QPushButton("+ Add Item")
        self.allButton = QPushButton("SVE")
        self.drinksButton = QPushButton("PICE")
        self.foodbutton = QPushButton("HRANA")

        columns = get_column_string(self.column_list)
        self.form = MenuForm(tableName, columns, self.rFrame)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        self.addItem.setStyleSheet(add)
        
        # --------FILL-LAYOUTS----------
        self.fill_llayout(QLabel(" "), self.allButton, self.drinksButton, self.foodbutton, QLabel(" "), self.textBox)
        self.fill_rtop(self.search, self.addItem)
        self.fill_rlayout(self.tableWidget)
        
        self.addItem.clicked.connect(self.on_click)
        self.drinksButton.pressed.connect(lambda: self.show_drinks(tableName))

    def on_click(self):
        self.form.textBox  = self.textBox
        self.form.table = self.tableWidget
        self.form.col_list = self.column_list
        self.form.show()

    def show_drinks(self, tableName):
        with Connection() as handler:
            query, self.rows = handler.select("*", tableName, "artikal_tip = 'Pice'")
        for row in self.rows:
            print(row)


class ScheduleMainView(MainView):
    def __init__(self, tableName):
        super().__init__(tableName)
        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.addButton = QPushButton("Edit Raspored")
        self.weekButton = QPushButton("Pregled Sedmice")

        columns = get_column_string(self.column_list)
        self.addForm = ScheduleAddForm(tableName,columns)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)

        # --------FILL-LAYOUTS----------  
        self.fill_llayout(self.calendar, self.addButton, self.weekButton, self.textBox)
        self.fill_rlayout(self.tableWidget)

        self.addButton.clicked.connect(self.addForm.show)

class ReservationMainView(MainView):
    def __init__(self, tableName):
        super().__init__(tableName)
        # override default MainView frames
        self.tFrame = MyFrame(QVBoxLayout)
        self.rFrame = MyFrame(QGridLayout)

        # ---------WIDGETS--------------
        self.icon= QIcon("assets/freeTable.png")
        columns = get_column_string(self.column_list)
        self.addForm = ReservationAddForm(tableName, columns)

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
        self.freeLabel.setStyleSheet(qss)
        self.calendar.setStyleSheet(cal)
        self.slider.setRange(0, 10) # 20 ticks
        self.rFrame.setObjectName("frame1")
        self.tFrame.setObjectName("frame2")

        # --------FILL-LAYOUTS----------
        self.fill_llayout(QLabel(" "),self.calendar, self.textBox,self.freeLabel, self.reservedLabel, self.takenLabel)
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
        self.rFrame.layout.addWidget(self.filler, 2, 3)

class ReceiptMainView(MainView):
    def __init__(self, tableName):
        super().__init__(tableName)
        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.search = QLineEdit()
        self.button = QPushButton("Simuliraj Narudzbe")

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)
        self.search.setStyleSheet(search)

        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.calendar, self.button, self.textBox)
        self.fill_rtop(self.search)
        self.fill_rlayout(self.tableWidget)
    
class WorkersMainView(MainView):
    def __init__(self, tableName): 
        super().__init__(tableName)
        # ---------WIDGETS--------------
        self.buttons = [QPushButton(label) for label in ["Svi","Servis","Kuhinja","Pomocni"]]
        self.addWorkerButton = QPushButton("+ Novi Radnik")
        self.search = QLineEdit()

        columns = get_column_string(self.column_list)
        self.workerForm = WorkerAddForm(tableName, columns)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        self.addWorkerButton.setStyleSheet("QPushButton{max-width:120px;}")

        # --------FILL-LAYOUTS----------
        self.fill_llayout(QLabel(" "),self.buttons[0],self.buttons[1],self.buttons[2], self.buttons[3],  QLabel(" "), self.textBox)
        self.fill_rtop(self.search, self.addWorkerButton)
        self.fill_rlayout(self.tableWidget)

        # --------BUTTON-ACTIONS--------
        self.addWorkerButton.clicked.connect(self.workerForm.show)