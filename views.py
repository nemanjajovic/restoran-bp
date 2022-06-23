from styles import *
from table import TableModel
from PySide6.QtWidgets import *
from PySide6 import QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QIcon
#from db import Connection
from forms import *

class MainView(QtWidgets.QWidget):
    """ Main layout template for all seperate views."""

    def __init__(self, viewName):
        super().__init__()
        #   Takes one argument, which represents the
        #   name of the child view.
        self.textBox = QTextEdit()

        # ----------LAYOUTS----------
        self.layout = QHBoxLayout()  # parent
        self.llayout = QVBoxLayout() # left
        self.rlayout = QVBoxLayout() # right

        self.layout.addLayout(self.llayout)
        self.layout.addLayout(self.rlayout)

        self.setLayout(self.layout)

        # ----------FRAMES-----------
        self.lFrame = MyFrame(QVBoxLayout) # left
        self.rFrame = MyFrame(QVBoxLayout) # right
        self.tFrame = MyFrame(QHBoxLayout) # top (right)

        # ----------WIDGET-----------
        self.nameLabel = QLabel(viewName)

        # ----------STYLES-----------
        self.llayout.setAlignment(Qt.AlignTop)
        self.llayout.setContentsMargins(0, 0, 0, 0)
        self.lFrame.layout.setAlignment(Qt.AlignTop)
        self.tFrame.layout.setAlignment(Qt.AlignLeft)
        self.nameLabel.setStyleSheet("QLabel{max-height:47px;padding-left:5px;font-size:20pt;}")
        
        # make all frames share the same properties
        for i, frame in enumerate([self.lFrame, self.rFrame, self.tFrame]):
            frame.setObjectName(f"frame{i}")
            frame.setFrameShape(QFrame.Box)
            frame.setFrameShadow(QFrame.Sunken)

    def fill_llayout(self, *widgets):
        # view name in top left, out of lFrame
        #self.llayout.addWidget(self.nameLabel)
        widgets = list(widgets)
        widgets.insert(0,self.nameLabel)
        self.fill(self.lFrame, self.llayout, widgets)
    
    def fill_rlayout(self, *widgets):
        self.fill(self.rFrame, self.rlayout, widgets)

    def fill_rtop(self, *widgets):
        self.fill(self.tFrame, self.rlayout, widgets)

    def fill(self, frame, layout, widgets):
        layout.addWidget(frame)
        for widget in widgets:
            frame.layout.addWidget(widget)

    def button_click(self):
        self.textBox.append(self.sender().text())

class MyFrame(QtWidgets.QFrame):
    """ Class that wraps a QFrame around a QBoxlayout 
        to make it easier to style. """

    def __init__(self, orientation):
        super().__init__()
        # ---------LAYOUT---------
        self.layout = orientation(self)
        self.setLayout(self.layout)
        
        # ---------STYLE----------
        darkTheme = DarkTheme(self.palette())
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet(qss)

class SliderLabel(QtWidgets.QWidget):
    """ Widget that contains labels for the slider."""
    def __init__(self):
        super().__init__()

        hbox = QHBoxLayout(self)
        hbox.setAlignment(Qt.AlignJustify)

        labels = [QLabel(str(i)) for i in range(1,13)]
        for label in labels:
            label.setFixedWidth(30)
            hbox.addWidget(label)

class MenuMainView(MainView):
    def __init__(self):
        super().__init__("Meni")
        # this is just a placeholder
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
            self.buttons[i].setFixedSize(QSize(140,130))
            self.buttons[i].setIconSize(QSize(140,130))
            
        self.buttons[0].clicked.connect(lambda:self.test(0))

        self.addButton = QPushButton("+ Reservation")
        self.tlocrt = QLabel("Tlocrt") # placeholder
        self.calendar = QCalendarWidget()
        sliderLbl = SliderLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.infoLabels = QLabel("""
                - Slobodno
                - Zauzeto
                - Rezervisano""")

        # ---------STYLES---------------
        self.tlocrt.setStyleSheet(tlo)
        self.calendar.setStyleSheet(cal)
        self.infoLabels.setAlignment(Qt.AlignBottom)
        self.slider.setRange(0, 20) # 20 ticks

        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.calendar,self.addButton,self.infoLabels, self.textBox)
        self.fill_rtop(sliderLbl, self.slider)
        #self.fill_rlayout(self.tlocrt)     
        self.fill_grid()
        self.addButton.clicked.connect(self.addForm.show)

    def test(self, n):
        print(n)

    def fill_grid(self):
        self.rlayout.addWidget(self.rFrame)
        x = 0
        for i in range(6):
            for j in range(5):
                self.rFrame.layout.addWidget(self.buttons[x],i,j)
                x += 1


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
        # self.rlayout.setObjectName(f"frame{i}")
        # self.rlayout.setFrameShape(QFrame.Box)
        # self.rlayout.setFrameShadow(QFrame.Sunken)

        # --------FILL-LAYOUTS----------
        self.fill_llayout(self.calendar, self.button, self.textBox)
        self.fill_rtop(self.search)
        self.fill_rlayout(self.table)
        

    
class WorkersMainView(MainView):
    def __init__(self):
        super().__init__("Radnici")
        # this is just a placeholder
        columns = ["gasdgsad", "shdah", "ASF"]

        # ---------WIDGETS--------------
        b1 = QPushButton("Svi")
        b2 = QPushButton("Servis")
        b3 = QPushButton("Kuhinja")
        b4 = QPushButton("Pomocni")
        self.search = QLineEdit()

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)

        # --------FILL-LAYOUTS----------
        self.fill_llayout(b1,b2,b3,b4, self.textBox)
        self.fill_rtop(self.search)
        self.fill_rlayout(self.table)

        b1.clicked.connect(lambda:self.test(b1.text()))
    
    def test(self, name):
        # test prints 'Svi'
        print(name)

