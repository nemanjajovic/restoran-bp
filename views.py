from styles import *
from table import TableModel
from PySide6.QtWidgets import *
from PySide6 import QtWidgets

class MainView(QtWidgets.QWidget):
    """ Main layout template for all seperate views."""

    def __init__(self, viewName):
        super().__init__()
        #   Takes one argument, which represents the
        #   name of the child view.

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

        # make all frames share the same properties
        for frame in [self.lFrame, self.rFrame, self.tFrame]:
            frame.setObjectName("frame")
            frame.setFrameShape(QFrame.Box)
            frame.setFrameShadow(QFrame.Sunken)

    def fill_llayout(self, *widgets):
        # view name in top left, out of lFrame
        self.llayout.addWidget(self.nameLabel)
        self.fill(self.lFrame, self.llayout, widgets)
    
    def fill_rlayout(self, *widgets):
        self.fill(self.rFrame, self.rlayout, widgets)

    def fill_rtop(self, *widgets):
        self.fill(self.tFrame, self.rlayout, widgets)

    def fill(self, frame, layout, widgets):
        layout.addWidget(frame)
        for widget in widgets:
            frame.layout.addWidget(widget)

class MyFrame(QtWidgets.QFrame):
    """ Class that wraps a QFrame around a QBoxlayout 
        to make it easier to style. """

    def __init__(self, orientation):
        super().__init__()
        # ---------LAYOUT---------
        self.layout = orientation(self)
        self.setLayout(self.layout)
        
        # ---------STYLE----------
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet(qss)

class SliderLabel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setAlignment(Qt.AlignJustify)
        labels = [QLabel(str(i)) for i in range(1,13)]
        for label in labels:
            label.setFixedWidth(30)
            hbox.addWidget(label)

class MenuMainView(MainView):
    def __init__(self):
        super().__init__("Meni")
        columns = ["gasdgsad", "shdah", "ASF"]
        # ---------WIDGETS--------------
        self.search = QLineEdit()
        self.addItem = QPushButton("+ Add Item")
        self.butt1 = QPushButton("PICE")
        self.butt2 = QPushButton("HRANA")

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.search.setStyleSheet(search)
        self.addItem.setStyleSheet(add)

        self.butt1.setFlat(True)
        self.butt2.setFlat(True)
        
        # --------FILL-LEFT-WIDGETS ----------
        self.fill_llayout(self.butt1,self.butt2)

        # --------ADD-RIGHT-WIDGETS ----------
        self.fill_rtop(self.search, self.addItem)
        self.fill_rlayout(self.table)

class ScheduleMainView(MainView):
    def __init__(self):
        super().__init__("Raspored")
        columns = ["gasdgsad", "shdah", "ASF"]

        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.weekButton = QPushButton("Sedmicni Raspored")

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)

        # -----ADD-LEFT-WIDGETS --------
        self.fill_llayout(self.calendar, self.weekButton)

        # ----ADD-RIGHT-WIDGETS --------
        self.fill_rlayout(self.table)

class ReservationMainView(MainView):
    def __init__(self):
        super().__init__("Rezervacije")
        # override default (horizontal) layout
        self.tFrame = MyFrame(orientation=QtWidgets.QVBoxLayout)

        # ---------WIDGETS--------------
        self.addButton = QPushButton("+ Reservation")
        self.tlocrt = QLabel("Tlocrt")
        self.calendar = QCalendarWidget()
        sliderLbl = SliderLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.infoLabels = QLabel("""
                - Free
                - Taken
                - Reserved""")

        # ---------STYLES---------------
        self.tFrame.setObjectName("frame")
        self.tlocrt.setStyleSheet(tlo)
        self.calendar.setStyleSheet(cal)
        self.infoLabels.setAlignment(Qt.AlignBottom)
        self.slider.setRange(0, 20)

        # -----ADD-LEFT-WIDGETS --------
        self.fill_llayout(self.addButton,self.calendar,self.infoLabels)

        # ----ADD-RIGHT-WIDGETS --------
        self.fill_rtop(sliderLbl, self.slider)
        self.fill_rlayout(self.tlocrt)              

class ReceiptMainView(MainView):
    def __init__(self):
        super().__init__("Racuni")
        columns = ["gasdgsad", "shdah", "ASF"]
        
        # ---------WIDGETS--------------
        self.calendar = QCalendarWidget()
        self.search = QLineEdit()

        self.table = QtWidgets.QTableView()
        self.tableWidget = TableModel(columns)
        self.table.setModel(self.tableWidget)

        # ---------STYLES---------------
        self.calendar.setStyleSheet(cal)
        self.search.setStyleSheet(search)

        # -----ADD-LEFT-WIDGETS --------
        self.fill_llayout(self.calendar)

        # ----ADD-RIGHT-WIDGETS --------
        self.fill_rtop(self.search)
        self.fill_rlayout(self.table)

class WorkersMainView(MainView):
    def __init__(self):
        super().__init__("Radnici")
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
        self.search.setStyleSheet(qss)

        # -----ADD-LEFT-WIDGETS --------
        self.fill_llayout(b1,b2,b3,b4)

        # ----ADD-RIGHT-WIDGETS --------
        self.fill_rtop(self.search)
        self.fill_rlayout(self.table)

        b1.clicked.connect(lambda:self.test(b1.text()))
    
    def test(self, name):
        print(name)

