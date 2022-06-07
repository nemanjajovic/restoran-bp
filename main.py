import sys
from styles import textInput
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QLineEdit,
    QWidget,
    QHBoxLayout,
) 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("My App")
        self.label = QLabel()
        self.label.setStyleSheet(textInput)
        
        layout = QHBoxLayout() 
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()