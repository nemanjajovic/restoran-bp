from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class DarkTheme():
    def __init__(self, palette):
        super().__init__()
        self.pal = palette
        self.pal.setColor(QPalette.Window, QColor(53, 53, 53))
        self.pal.setColor(QPalette.WindowText, Qt.white)
        self.pal.setColor(
            QPalette.Disabled, QPalette.WindowText, QColor(127, 127, 127)
        )
        self.pal.setColor(QPalette.Base, QColor(42, 42, 42))
        self.pal.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        self.pal.setColor(QPalette.ToolTipBase, Qt.white)
        self.pal.setColor(QPalette.ToolTipText, Qt.white)
        self.pal.setColor(QPalette.Text, Qt.white)
        self.pal.setColor(
            QPalette.Disabled, QPalette.Text, QColor(127, 127, 127)
        )
        self.pal.setColor(QPalette.Dark, QColor(35, 35, 35))
        self.pal.setColor(QPalette.Shadow, QColor(20, 20, 20))
        self.pal.setColor(QPalette.Button, QColor(53, 53, 53))
        self.pal.setColor(QPalette.ButtonText, Qt.white)
        self.pal.setColor(
            QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127)
        )
        self.pal.setColor(QPalette.BrightText, Qt.red)
        self.pal.setColor(QPalette.Link, QColor(42, 130, 218))
        self.pal.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.pal.setColor(
            QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80)
        )
        self.pal.setColor(QPalette.HighlightedText, Qt.white)
        self.pal.setColor(
            QPalette.Disabled,
            QPalette.HighlightedText,
            QColor(127, 127, 127),
        )

qss1 = """
    max-width:400px;
    min-width:300px;
    border :3px solid darkblue;
"""
qss = """
        QFrame#frame{border: 2px solid green; border-radius: 4px;}
        QFrame#frame::Hover{border: 2px solid white;}
        QLineEdit{border: 2px solid green; border-radius: 4px;}
        QLineEdit::Hover{border: 2px solid white;}
        """

search = """
    max-width:300px;
"""
add = """
    max-width:100px;
"""
menu = """
    text-align:left;
"""
cal = """
    max-width:310px;
    max-height:250px;
"""

tlo = """
    min-width:600px;
    min-height:400px;
    border :2px solid blue;
"""
naslov= """
    max-height: 20px;
"""

