from PySide6.QtWidgets import *
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel
from PySide6.QtGui import QPixmap, QIcon, QMouseEvent
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
        self.tableWidget = Table(tableName, self.rows, self.column_list, self.textBox, "")

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
    """ A window parent class to all data entry/editing forms, used also as a
        database interface."""
    def __init__(self, tableName, columns, textBox):
        super().__init__()
        self.tableName = tableName
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

    def show_all(self):
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.select("*", self.tableName, "")
        self.replace_table(rows, column_list, "")
        self.update_textbox(query)

    def replace_table(self, rows, column_list, cond):
        _widget = self.rFrame.layout.takeAt(0)
        _widget.widget().deleteLater()
        self.table = Table(self.tableName, rows, column_list, self.textBox, cond)
        self.rFrame.layout.addWidget(self.table)

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
    def __init__(self, name, rows, columns, textBox, cond):
        super().__init__(len(rows),len(columns))
        self.cond = cond
        self.column_dict = {}
        self.tableName = name
        self.textBox = textBox
        # (program width - left frame) / nr of col
        col_width = int(865/len(columns))

        # ----------STYLES---------
        self.setHorizontalHeaderLabels(columns)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setMinimumSectionSize(col_width)
        self.setStyleSheet("QHeaderView {margin-left: 12px }")

        self.horizontalHeader().sectionClicked.connect(self.headerOnClick)
        
        self.init_dict(columns)
        self.populate_table(rows, columns)
    
    def init_dict(self, columns):
        for i, _ in enumerate(columns):
            self.column_dict[i] = "ASC"
        self.column_dict[0] = "DESC"

    def populate_table(self, rows, col):
        for i, row in enumerate(rows):
            for j in range(len(col)):
                item = QTableWidgetItem(str(row[j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.setItem(i, j, item)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)
        index = self.indexAt(event.pos())
        if index.isValid():
            self.show_table_form(index.row())

    def show_table_form(self, row):
        with Connection() as handler:
            column_list , columns = handler.get_column_names(self.tableName)
        self.tableForm = TableInfoForm(self, row, column_list, columns, self.textBox)
        self.tableForm.show()

    def headerOnClick(self, i):
        with Connection() as handler:
            column_list, _ = handler.get_column_names(self.tableName)
            query, rows = handler.order_by(self.tableName, f"{column_list[i]} {self.column_dict[i]}", self.cond)
        self.switch_order(i)
        self.populate_table(rows, column_list)
        self.textBox.append(query)
        self.textBox.append(dash)

    def switch_order(self, i):
        if self.column_dict[i] == "ASC":
            self.column_dict[i] = "DESC"
        else:
            self.column_dict[i] = "ASC"

class TableInfoForm(MainForm):
    """ An info form window for the individual restaurant tables."""

    def __init__(self, table, row, column_list, columns, textBox):
        super().__init__(table, columns, textBox)

        self.init_values = []
        self.column_list = column_list
        self.tableName = table.tableName
        self.populate_table = table.populate_table

        # ---------WIDGETS----------
        label_list = [QLabel(text) for text in column_list]
        self.le_list = [QLineEdit() for col in column_list]
        delButton = QPushButton("Izbrisi")
        saveButton = QPushButton("Sačuvaj")
        
        # ----------LAYOUT----------
        for i, l in enumerate(label_list):
            cell_str = table.item(row, i).text()
            self.init_values.append(cell_str)
            self.le_list[i].insert(cell_str)
            self.le_list[i].setModified(False)
            self.layout.addWidget(l, i, 0)
            self.layout.addWidget(self.le_list[i], i, 1)

        self.layout.addWidget(saveButton,len(self.le_list),1)
        self.layout.addWidget(delButton,len(self.le_list),0)

        # ----------STYLE-----------
        self.setStyleSheet("QLabel{font-size:16px}")
        self.setFixedSize(500,340)
        self.le_list[0].setReadOnly(True)

        saveButton.clicked.connect(lambda: self.save_changes())

    def closeEvent(self, event):
        can_exit = self.data_not_changed()
        while not can_exit:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Promjene")
            dlg.setText("Sačuvaj promjene?")
            dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            dlg.setIcon(QMessageBox.Question)
            button = dlg.exec()
            
            if button == QMessageBox.Yes:
                self.save_changes()
                can_exit = True
            else:
                can_exit = True

    def data_not_changed(self):
        current_values = self.get_line_edit()
        return self.init_values == current_values

    def del_row(self):
        _, whereValue = self.get_sql_values()
        with Connection() as handler:
            query = handler.delete(self.tableName, whereValue)
            self.textBox.append(query)
            self.textBox.append(dash)
            query, rows = handler.select("*", self.tableName, "")
        self.populate_table(rows, self.column_list)
        self.textBox.append(query)
        self.textBox.append(dash)
        
    def save_changes(self):
        setValue, whereValue = self.get_sql_values()
        with Connection() as handler:
            query = handler.update(self.tableName, setValue, whereValue)
            self.textBox.append(query)
            self.textBox.append(dash)
            query, rows = handler.select("*", self.tableName, "")
        self.populate_table(rows, self.column_list)
        self.textBox.append(query)
        self.textBox.append(dash)
        self.init_values = self.get_line_edit()

    def get_sql_values(self):
        """ Returns two strings, one for the SET SQL command, 
            the other for the WHERE condition."""

        changed_columns, changed_values = self.get_changed()
        setString = self.make_string(changed_columns, changed_values)
        whereValue = f"{self.column_list[0]}={self.le_list[0].text()}"
        return setString, whereValue
    
    def get_changed(self):
        """ Returns two lists, one is the changed columns and
            the other their new values."""

        current_values = self.get_line_edit()
        changed_values = list(set(current_values)-set(self.init_values))
        changed_columns = [self.column_list[current_values.index(elem)] for elem in changed_values]
        return changed_columns, changed_values

    # format the SQL SET command arguments
    def make_string(self, col, val):
        setString = ""
        for column, value in zip(col, val):
            setString += f"{column}='{value}',"
        setString = setString[:-1]
        return setString

    def get_line_edit(self):
        return [self.le_list[i].text() for i in range(len(self.le_list))]

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