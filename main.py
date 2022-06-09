import sys
from styles import *
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QLineEdit,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
) 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("My App")
        self.label = QLabel()
        self.label.setStyleSheet(qss1)
        self.label2 = QLabel()
        self.label2.setStyleSheet(qss2)
        
        layout = QHBoxLayout()
        layout_left = QVBoxLayout()
        layout_right = QVBoxLayout()

        layout.addLayout(layout_left)
        layout.addLayout(layout_right)

        layout_left.addWidget(self.label)
        layout_right.addWidget(self.label2)

        container = QWidget()
        container.setLayout(layout)

        menu = self.menuBar()
        menuItems = ["Meni","Rezervacije","Racuni","Radnici","About"]
        for m in menuItems:
            file_menu = menu.addMenu(m)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()