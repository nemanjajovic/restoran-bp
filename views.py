from styles import *
from helper_widgets import *
from PySide6.QtWidgets import *
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon
from db import Connection
from forms import *

class MenuMainView(MainView):
    def __init__(self, tableName):
        super().__init__(tableName)
        # ---------WIDGETS--------------
        self.search = QLineEdit()
        addItem = QPushButton("+ Add Item")
        allButton = QPushButton("SVE")
        drinksButton = QPushButton("PICE")
        foodButton = QPushButton("HRANA")

        columns = get_column_string(self.column_list)
        self.form = MenuForm(tableName, columns, self.rFrame, self.textBox)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        addItem.setStyleSheet(add)
        
        # --------FILL-LAYOUTS----------
        self.fill_llayout(QLabel(" "), allButton, drinksButton, foodButton, QLabel(" "), self.textBox)
        self.fill_rtop(self.search, addItem)
        self.fill_rlayout(self.tableWidget)
        
        # ---------CONNECTIONS----------
        addItem.clicked.connect(self.form.show)
        allButton.pressed.connect(self.form.show_all)
        drinksButton.pressed.connect(self.form.show_drinks)
        foodButton.pressed.connect(self.form.show_food)

class ScheduleMainView(MainView):
    def __init__(self, tableName):
        super().__init__(tableName)
        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.addButton = QPushButton("Edit Raspored")
        self.weekButton = QPushButton("Pregled Sedmice")

        columns = get_column_string(self.column_list)
        self.addForm = ScheduleAddForm(tableName,columns, self.textBox)

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
        self.addForm = ReservationAddForm(tableName, columns, self.textBox)

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
        allButton = QPushButton("Svi")
        serviceButton = QPushButton("Servis")
        kitchenButton = QPushButton("Kuhinja")
        helperButton = QPushButton("Pomoćni")
        addWorkerButton = QPushButton("+ Novi Radnik")
        self.search = QLineEdit()

        columns = get_column_string(self.column_list)
        self.workerForm = WorkerAddForm(tableName, columns, self.rFrame, self.textBox)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        addWorkerButton.setStyleSheet("QPushButton{max-width:120px;}")

        # --------FILL-LAYOUTS----------
        self.fill_llayout(QLabel(" "), allButton, serviceButton, kitchenButton, helperButton,  QLabel(" "), self.textBox)
        self.fill_rtop(self.search, addWorkerButton)
        self.fill_rlayout(self.tableWidget)

        # --------CONNECTIONS-----------
        addWorkerButton.clicked.connect(self.workerForm.show)
        allButton.clicked.connect(self.workerForm.show_all)
        serviceButton.clicked.connect(self.workerForm.show_service)
        kitchenButton.clicked.connect(self.workerForm.show_kitchen)
        helperButton.clicked.connect(self.workerForm.show_helpers)