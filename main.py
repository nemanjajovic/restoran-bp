import sys
from styles import *
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel
from PySide6.QtGui import QAction
from PySide6.QtWidgets import *
from views import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("My App")

        self.layout = QHBoxLayout()
        defaultView = ReceiptMainView()
        self.setView(defaultView)

        container = QWidget()
        container.setLayout(self.layout)
        
        views = {
            "menu": QAction("Meni",self),
            "rezervacije": QAction("Raspored",self),
            "raspored": QAction("Rezervacije",self),
            "racuni": QAction("Racuni",self),
            "radnici": QAction("Radnici",self),
        }
        file = {
            "mkbkp": QAction("Make Backup",self),
            "opbkp": QAction("Open Backup",self),
            "opt":   QAction("Settings",self),
            "exit":   QAction("Exit",self),
        }
        menu = self.menuBar()

        # ----------ADD-MENUS-----------------
        self.file_menu = menu.addMenu("File")
        self.views_menu = menu.addMenu("View")
        self.about_menu = menu.addMenu("About")

        # ----------ADD-MENU-ACTIONS---------------
        self.file_menu.addAction(file["mkbkp"])
        self.file_menu.addAction(file["opbkp"])
        self.file_menu.addAction(file["opt"])
        self.file_menu.addAction(file["exit"])
        self.views_menu.addAction(views["menu"])
        self.views_menu.addAction(views["raspored"])
        self.views_menu.addAction(views["rezervacije"])
        self.views_menu.addAction(views["racuni"])
        self.views_menu.addAction(views["radnici"])

        # Set the central widget of the Window.
        self.setCentralWidget(container)
        #self.showFullScreen()

        

    def p(self, s):
        print("dgasdsgsgd")

    def setView(self, View):
        self.layout.addLayout(View.llayout)
        self.layout.addLayout(View.rlayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.setStyle("Fusion")
    app.exec()