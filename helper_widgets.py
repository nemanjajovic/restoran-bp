import pandas as pd
from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel
from PySide6.QtGui import QPixmap, QIcon
from styles import *

class MainView(QWidget):
    """ A layout parent class for all views, takes one string
        argument which represents the name of the view."""
    def __init__(self, viewName):
        super().__init__()
        # ----------WIDGETS----------
        self.nameLabel = QLabel(viewName)
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

        # ----------STYLES-----------
        self.llayout.setAlignment(Qt.AlignTop)
        self.llayout.setContentsMargins(0, 0, 0, 0)
        self.lFrame.layout.setAlignment(Qt.AlignTop)
        self.tFrame.layout.setAlignment(Qt.AlignLeft)
        self.nameLabel.setStyleSheet("QLabel{max-height:47px;padding-left:5px;font-size:20pt;}")
        
        # set frame names
        for i, frame in enumerate([self.lFrame, self.rFrame, self.tFrame]):
            frame.setObjectName(f"frame{i}")

    def fill_llayout(self, *widgets):
        widgets = list(widgets)
        widgets.insert(0,self.nameLabel) # make first widget
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

class MyFrame(QFrame):
    """ A class that wraps a QFrame around a QBoxLayout 
        to make it easier to style, takes one QBoxLayout
        as an argument."""
    def __init__(self, layout):
        super().__init__()
        # ---------LAYOUT---------
        self.layout = layout(self)
        self.setLayout(self.layout)
        
        # ---------STYLE----------
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet(qss)

class SliderLabel(QWidget):
    """ Widget that contains time labels for the slider."""
    def __init__(self):
        super().__init__()

        hbox = QHBoxLayout(self)
        hbox.setAlignment(Qt.AlignJustify)
        time = []
        for i in range(1,11):
            time.append(str(i))
        time.insert(0,"12")

        labels = [QLabel(i) for i in time]
        for label in labels:
            label.setFixedWidth(73)
            label.setStyleSheet("QLabel{font-size:16px;}")
            label.setAlignment(Qt.AlignCenter)
            hbox.addWidget(label)

class MainForm(QMainWindow):
    """ A window parent class to all data entry/editing forms."""
    def __init__(self):
        super().__init__()
        # layout needs to be inside a widget to be displayed properly
        centralWidget = QWidget()

        # ----------LAYOUT-----------
        self.layout = QGridLayout()
        centralWidget.setLayout(self.layout)

        # ----------STYLE------------
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Form")
        self.setFixedSize(640,320)
        self.setStyleSheet(qss)

        self.setCentralWidget(centralWidget)

    def insert(self, table, columns, values):
        with Connection() as handler:
            handler.insert(table, columns, values)

    def update(self, table, column, new_val, id_column, id_val):
        with Connection() as handler:
            handler.update(table, column, new_val, id_column, id_val)

class TableModel(QAbstractTableModel):
    def __init__(self, col=[], rows=[]):
        super().__init__()
        self._data = pd.DataFrame(
            [],
            columns = col,
            index = rows,
        )

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class IconLabel(QWidget):
    """A class combining an icon and text."""
    def __init__(self, icon_path, text, final_stretch=True):
        super().__init__()
        IconSize = QSize(24, 24)
        HorizontalSpacing = 2

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        icon = QLabel()
        icon.setPixmap(QIcon(icon_path).pixmap(IconSize))

        layout.addWidget(QLabel("                                      "))      
        layout.addWidget(icon)
        layout.addWidget(QLabel(text))

        if final_stretch:
            layout.addStretch()

class Reservations():
    def __init__(self):
        super().__init__()

        self.hours = {
            "12": None,
            "1":  None,
            "2":  None,
            "3":  None,
            "4":  None,
            "5":  None,
            "6":  None,
            "7":  None,
            "8":  None,
            "9":  None,
            "10": None,
        }