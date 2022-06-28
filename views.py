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
        # column names
        with Connection() as handler:
            column_list, columns = handler.get_column_names(tableName)
            query, rows = handler.select("*", tableName, "")
        t = [[None for i in range(len(column_list))]]
        super().__init__(tableName)
        columns = self.get_column_string(column_list)

        #---------FORM-WINDOW-----------
        self.form = MenuForm(tableName, columns)

        # ---------WIDGETS--------------
        self.search = QLineEdit()
        self.addItem = QPushButton("+ Add Item")
        self.allButton = QPushButton("SVE")
        self.drinksButton = QPushButton("PICE")
        self.foodbutton = QPushButton("HRANA")

        self.tableWidget = Table(rows, column_list)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        self.addItem.setStyleSheet(add)
        
        # --------FILL-LAYOUTS----------
        self.fill_llayout(QLabel(" "), self.allButton, self.drinksButton, self.foodbutton, QLabel(" "), self.textBox)
        self.fill_rtop(self.search, self.addItem)
        self.fill_rlayout(self.tableWidget)
        
        self.addItem.clicked.connect(self.form.show)

        self.textBox.append(query)
        self.textBox.append("---------------------------------------------------")

class ScheduleMainView(MainView):
    def __init__(self, tableName):
        with Connection() as handler:
            column_list, columns = handler.get_column_names(tableName)
        t =[ [None for i in range(len(column_list))]]
        super().__init__(tableName)
        columns = self.get_column_string(column_list)
        self.addForm = ScheduleAddForm(tableName,columns)

        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.addButton = QPushButton("Edit Raspored")
        self.weekButton = QPushButton("Pregled Sedmice")

        #self.table = QtWidgets.QTableView()
        #self.tableWidget = Table(rows, columns)
        #self.tableWidget.populate_table()

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)

        # --------FILL-LAYOUTS----------  
        self.fill_llayout(self.calendar, self.addButton, self.weekButton, self.textBox)
        #self.fill_rlayout(self.table)

        self.addButton.clicked.connect(self.addForm.show)

class ReservationMainView(MainView):
    def __init__(self, tableName):
        with Connection() as handler:
            column_list, columns = handler.get_column_names(tableName)
        super().__init__(tableName)
        columns = self.get_column_string(column_list)
        # override default (horizontal) MainView layout
        self.tFrame = MyFrame(QVBoxLayout)
        self.tFrame.setObjectName("frame2")
        self.addForm = ReservationAddForm(tableName, columns)
        
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
        self.freeLabel.setStyleSheet(qss)
        self.calendar.setStyleSheet(cal)
        self.slider.setRange(0, 10) # 20 ticks
        self.rFrame.setObjectName(f"frame{1}")

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
        with Connection() as handler:
            column_list, columns = handler.get_column_names(tableName)
        t = [[None for i in range(len(column_list))]]
        super().__init__(tableName)
        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.search = QLineEdit()
        self.button = QPushButton("Simuliraj Narudzbe")

        self.table = QtWidgets.QTableView()
        self.tableWidget = QTableWidget(len(t),len(column_list))
        self.tableWidget.setHorizontalHeaderLabels(column_list)
        #self.tableWidget.horizontalHeaderItem().setTextAlignment(Qt.AlignHCenter)
        # for i, row in enumerate(rows):
        #     for j in range(len(column_list)):
        #             self.tableWidget.setItem(i, j, QTableWidgetItem(str(row[j])))

        self.tableWidget.verticalHeader().setVisible(False)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)
        self.search.setStyleSheet(search)

        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.calendar, self.button, self.textBox)
        self.fill_rtop(self.search)
        self.fill_rlayout(self.tableWidget)
    
class WorkersMainView(MainView):
    def __init__(self, tableName):
        with Connection() as handler:
            column_list, columns = handler.get_column_names(tableName)
            query, rows = handler.select("*", tableName, "")        
        super().__init__(tableName)
        columns = self.get_column_string(column_list)
        self.workerForm = WorkerAddForm(tableName, columns)

        # ---------WIDGETS--------------
        self.buttons = [QPushButton(label) for label in ["Svi","Servis","Kuhinja","Pomocni"]]
        self.addWorkerButton = QPushButton("+ Novi Radnik")
        self.search = QLineEdit()

        self.tableWidget = Table(rows, column_list)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        #self.tableWidget.setStyleSheet("""QWidget {background-color: #333333;color: #fffff8; }""")
        self.addWorkerButton.setStyleSheet("QPushButton{max-width:120px;}")

        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.buttons[0],self.buttons[1],self.buttons[2],self.buttons[3], self.textBox)
        self.fill_rtop(self.search, self.addWorkerButton)
        self.fill_rlayout(self.tableWidget)

        # --------BUTTON-ACTIONS--------
        self.addWorkerButton.clicked.connect(self.workerForm.show)

        self.textBox.append(query)