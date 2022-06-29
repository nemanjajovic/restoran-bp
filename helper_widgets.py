import pandas as pd
from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel
from PySide6.QtGui import QPixmap, QIcon
from styles import *
from db import Connection

class MainView(QWidget):
    """ A layout parent class for all views, takes one string
        argument which represents the name of the view."""

    def __init__(self, tableName):
        super().__init__()
        self.tableName = tableName
        # first query to get all rows and query string
        with Connection() as handler:
            self.column_list, _ = handler.get_column_names(tableName)
            self.query, self.rows = handler.select("*", tableName, "")

        # ----------WIDGETS----------
        self.nameLabel = QLabel(tableName)
        self.textBox = QTextEdit()
        self.tableWidget = Table(self.rows, self.column_list)

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
        self.textBox.setStyleSheet("QTextEdit{background:#404040}")
        self.textBox.setReadOnly(True)
        self.nameLabel.setStyleSheet("QLabel{max-height:47px;padding-left:5px;font-size:20pt;}")
        
        # set frame names
        for i, frame in enumerate([self.lFrame, self.rFrame, self.tFrame]):
            frame.setObjectName(f"frame{i}")

        self.update_textbox(self.query)

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

    def update_textbox(self, query):
        self.textBox.append(query)
        self.textBox.append(dash)

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
        self.setStyleSheet(qss+"QFrame{background-color: #333333;}")

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
    def __init__(self, table, columns, textBox):
        super().__init__()
        self.tableName = table
        # layout needs to be inside a widget to be displayed properly
        centralWidget = QWidget()
        self.textBox = textBox

        # ----------LAYOUT-----------
        self.layout = QGridLayout()
        centralWidget.setLayout(self.layout)

        # ----------STYLE------------
        #self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Form")
        self.setFixedSize(640,320)
        self.setStyleSheet(qss)

        self.setCentralWidget(centralWidget)

    def insert(self, columns, values):
        with Connection() as handler:
            query, _ = handler.insert(self.tableName, columns, values)
            self.update_textbox(query)

    def update(self, column, new_val, id_column, id_val):
        with Connection() as handler:
            handler.update(self.tableName, column, new_val, id_column, id_val)

    def replace_table(self, rows, column_list):
        _widget = self.rFrame.layout.takeAt(0)
        _widget.widget().deleteLater()
        self.table = Table(rows, column_list)
        self.rFrame.layout.addWidget(self.table)

    def show_all(self):
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, "")
        self.replace_table(rows, column_list)
        self.update_textbox(query)

    def update_textbox(self, query):
        self.textBox.append(query)
        self.textBox.append(dash)

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

class Table(QTableWidget):
    def __init__(self, rows, columns):
        super().__init__(len(rows),len(columns))
        self.rows = rows
        self.columns = columns
        # (program width - left frame) / nr of col
        col_width = int(865/len(columns))

        # ----------STYLES---------
        self.setHorizontalHeaderLabels(columns)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setMinimumSectionSize(col_width)
        self.setStyleSheet("QHeaderView {margin-left: 12px }")

        self.populate_table(rows, columns)

    def populate_table(self, rows, col):
        for i, row in enumerate(rows):
            for j in range(len(col)):
                item = QTableWidgetItem(str(row[j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j, item)


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

def get_column_string(list):
    string = ""
    for word in list[1:]:
        string += word + ','
    return string[:-1]