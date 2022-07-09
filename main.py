import sys
from styles import *
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *
from views import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        # ----------LAYOUT-----------
        self.layout = QStackedWidget()
        
        # add widgets on the stack
        self.layout.addWidget(MenuMainView("MeniArtikli"))
        self.layout.addWidget(ScheduleMainView("Raspored"))
        self.layout.addWidget(ReservationMainView("Rezervacije"))
        self.layout.addWidget(ReceiptMainView("Racuni"))
        self.layout.addWidget(WorkersMainView("Radnici"))

        # ----------STYLE-----------
        self.setWindowTitle("My App")
        self.layout.setCurrentIndex(0)
        
        # ----------------MENU-------------------
        menu = self.menuBar()
        
        # -----------MENU-ACTIONS----------------
        file = {
            "mkbkp": QAction("Make Backup",self),
            "opbkp": QAction("Open Backup",self),
            "opt":   QAction("Settings",self),
            "exit":   QAction("Exit",self),
        }
        views = {
            "menu": QAction("Meni",self),
            "raspored": QAction("Raspored",self),
            "rezervacije": QAction("Rezervacije",self),
            "racuni": QAction("Racuni",self),
            "radnici": QAction("Radnici",self),
        }

        # ----------ADD-MENU-ITEMS---------------
        self.file_menu = menu.addMenu("File")
        self.views_menu = menu.addMenu("View")
        self.about_menu = menu.addMenu("About")

        # ----------POPULATE-MENUS---------------
        self.populate_file(file)
        self.populate_views(views)

        # ---------CONNECT-ACTIONS---------------
        self.view_actions(views)

        # Set the central widget of the Window.
        self.setCentralWidget(self.layout)

    def populate_file(self, file):
        self.file_menu.addAction(file["mkbkp"])
        self.file_menu.addAction(file["opbkp"])
        self.file_menu.addAction(file["opt"])
        self.file_menu.addAction(file["exit"])
        
    def populate_views(self, views):
        self.views_menu.addAction(views["menu"])
        self.views_menu.addAction(views["raspored"])
        self.views_menu.addAction(views["rezervacije"])
        self.views_menu.addAction(views["racuni"])
        self.views_menu.addAction(views["radnici"])

    def view_actions(self, views):
        views["menu"].triggered.connect(lambda:self.switch_view(0))
        views["raspored"].triggered.connect(lambda:self.switch_view(1))
        views["rezervacije"].triggered.connect(lambda:self.switch_view(2))
        views["racuni"].triggered.connect(lambda:self.switch_view(3))
        views["radnici"].triggered.connect(lambda:self.switch_view(4))

    def switch_view(self, index):
        self.layout.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion") 

    window = MainWindow()
    window.setFixedSize(1240,800)
    #window.setWindowFlags(Qt.FramelessWindowHint)
    window.show()

    app.setStyleSheet(qss)
    app.exec()