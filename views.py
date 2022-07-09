from styles import *
from helper_widgets import *
from PySide6.QtWidgets import *
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon
from db import Connection
from forms import *
from data import itemCategories

class MenuMainView(MainView):
    def __init__(self, tableName):
        super().__init__(tableName)
        # ---------WIDGETS--------------
        self.search = QLineEdit()
        addItem = QPushButton("+ Add Item")
        tableNameLabel = QLabel(tableName)
        self.allButton = QPushButton("SVE")
        self.drinksButton = QPushButton("PICE")
        self.foodButton = QPushButton("HRANA")
        self.drinkButtons = list(map(self.button, itemCategories[0]))
        self.foodButtons = list(map(self.button, itemCategories[1]))

        columns = get_column_string(self.column_list)
        self.form = MenuForm(self.tableName, columns, self.rFrame, self.textBox)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        addItem.setStyleSheet(add)
        tableNameLabel.setStyleSheet("QLabel{max-height:47px;padding-left:5px;font-size:20pt;}")
        for button in self.drinkButtons:
            button.setStyleSheet("QPushButton{font-size:12px;max-width:200px;}")
        for button in self.foodButtons:
            button.setStyleSheet("QPushButton{font-size:12px;max-width:200px;}")
        
        # --------FILL-LAYOUTS----------
        self.fill_llayout(tableNameLabel, QLabel(" "), self.allButton, self.drinksButton, self.foodButton, QLabel(" "), self.textBox)
        self.fill_rtop(self.search, addItem)
        self.fill_rlayout(self.tableWidget)
        
        # ---------CONNECTIONS----------
        addItem.clicked.connect(lambda: self.show(columns))
        self.allButton.pressed.connect(self.allClick)
        self.drinksButton.pressed.connect(self.drinkClick)
        self.foodButton.pressed.connect(self.foodClick)
        self.search.returnPressed.connect(lambda: self.form.search(self.search.text()))

    def show(self, columns):
        self.form = MenuForm(self.tableName, columns, self.rFrame, self.textBox)
        self.form.show()

    def button(self, label):
        return QPushButton(label)

    def allClick(self):
        self.replace_llayout(QLabel(" "), self.allButton, self.drinksButton, self.foodButton, QLabel(" "), self.textBox)
        self.form.show_table("")

    def drinkClick(self):
        self.replace_llayout(QLabel(" "), self.allButton, self.drinksButton, self.drinkButtons[0],self.drinkButtons[1],self.drinkButtons[2],self.drinkButtons[3],self.drinkButtons[4],self.drinkButtons[5],self.drinkButtons[6],self.foodButton, QLabel(" "), self.textBox)
        self.form.show_table("artikal_tip='Pice'")

    def foodClick(self):
        self.replace_llayout(QLabel(" "), self.allButton, self.drinksButton, self.foodButton, self.foodButtons[0],self.foodButtons[1],self.foodButtons[2],self.foodButtons[3],self.foodButtons[4], QLabel(" "), self.textBox)
        self.form.show_table("artikal_tip='Hrana'")

class ScheduleMainView(MainView):
    def __init__(self, tableName):
        super().__init__(tableName)
        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        addButton = QPushButton("+ Dodaj")
        self.weekButton = QPushButton("Pregled Sedmice")

        self.columns = get_column_string(self.column_list)
        self.form = ScheduleAddForm(tableName, self.columns, self.calendar, self.rFrame, self.textBox)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)

        # --------FILL-LAYOUTS----------  
        self.fill_llayout(self.calendar, addButton, self.weekButton, self.textBox)
        self.fill_rlayout(self.tableWidget)

        # ----------CONNECTIONS----------
        addButton.clicked.connect(self.show)
        self.calendar.clicked.connect(self.select_date)

    def show(self):
        self.form.show()

    def select_date(self, date):
        self.form.show_date(date)
        self.form = ScheduleAddForm(self.tableName, self.columns, self.calendar, self.rFrame, self.textBox)

class ReservationMainView(MainView):
    def __init__(self, tableName):
        super().__init__(tableName)
        # override default MainView frames
        self.tFrame = MyFrame(QVBoxLayout)
        self.rFrame = MyFrame(QGridLayout)

        # ---------WIDGETS--------------
        self.icon= QIcon("assets/icons/freeTable.png")
        columns = get_column_string(self.column_list)
        self.addForm = ReservationAddForm(tableName, columns, self.textBox)

        self.buttons = []
        for i in range(20):
            self.buttons.append(QPushButton())
            butt = self.buttons[i]
            butt.setIcon(self.icon)
            butt.setFixedSize(QSize(100,100))
            butt.setIconSize(QSize(120,120))
            butt.pressed.connect(lambda i=i+1: self.tableWidget.show_table_form(i))
            
        self.addButton = QPushButton("+ Reservation")
        self.filler = QLabel()
        self.calendar = QCalendarWidget()
        sliderLbl = SliderLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.freeLabel = IconLabel("assets/icons/freeTable.png", "-  Slobodno")
        self.reservedLabel = IconLabel("assets/icons/reservedTable.png", "-  Rezervisano")
        self.takenLabel = IconLabel("assets/icons/takenTable.png", "-  Zauzeto")

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
        allButton = QPushButton("Prikaži Sve")
        calendar = QCalendarWidget()
        self.search = QLineEdit()
        self.button = QPushButton("Simuliraj Narudzbe")

        columns = get_column_string(self.column_list)
        self.form = ReceiptForm(tableName, columns, self.rFrame, self.textBox)

        # ---------STYLES---------------
        calendar.setStyleSheet(cal)
        self.search.setStyleSheet(search)

        # --------FILL-LAYOUTS----------
        self.fill_llayout(calendar, allButton, self.button, self.textBox)
        self.fill_rtop(self.search)
        self.fill_rlayout(self.tableWidget)

        allButton.pressed.connect(self.form.show_all)
        calendar.clicked.connect(self.form.show_date)
    
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
        self.form = WorkerForm(tableName, columns, self.rFrame, self.textBox)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        addWorkerButton.setStyleSheet("QPushButton{max-width:120px; margin-left:20px;}")

        # --------FILL-LAYOUTS----------
        self.fill_llayout(QLabel(" "), allButton, serviceButton, kitchenButton, helperButton,  QLabel(" "), self.textBox)
        self.fill_rtop(self.search, addWorkerButton)
        self.fill_rlayout(self.tableWidget)

        # --------CONNECTIONS-----------
        addWorkerButton.clicked.connect(lambda: self.show(columns))
        allButton.clicked.connect(self.form.worker_show_all)
        serviceButton.clicked.connect(lambda: self.form.show_table("radnik_tip='Servis'"))
        kitchenButton.clicked.connect(lambda: self.form.show_table("radnik_tip='Kuhinja'"))
        helperButton.clicked.connect(lambda: self.form.show_table("radnik_tip='Pomocni'"))
        self.search.returnPressed.connect(lambda: self.form.search(self.search.text()))

    def show(self, columns):
        self.form = WorkerForm(self.tableName, columns, self.rFrame, self.textBox)
        self.form.show()