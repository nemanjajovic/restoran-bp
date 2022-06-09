import sys
from styles import *
from PySide6.QtCore import QSize, Qt ,QAbstractTableModel
from PySide6.QtWidgets import *
from views import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("My App")

        self.layout = QHBoxLayout()
        defaultView = ReservationMainView()
        self.setView(defaultView)

        container = QWidget()
        container.setLayout(self.layout)

        menu = self.menuBar()
        menuItems = ["Meni","Rezervacije","Racuni","Radnici","About"]
        for m in menuItems:
            file_menu = menu.addMenu(m)

        # Set the central widget of the Window.
        self.setCentralWidget(container)
        #self.showFullScreen()

    def setView(self, View):
        self.layout.addLayout(View.llayout)
        self.layout.addLayout(View.rlayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.setStyle("Fusion")
    app.exec()