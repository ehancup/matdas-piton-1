from PyQt6.QtWidgets import QLineEdit, QLabel
from PyQt6.QtCore import Qt

class TextInput(QLineEdit):
    def __init__(self,label, placeholder="", parent=None):
        super().__init__(parent)
        self.label = label
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(40)
        self.setStyleSheet("font-size: 18px;")

    def getLabel(self):
        fxlabel = QLabel(self.label)
        fxlabel.setStyleSheet("font-size: 18px;")
        fxlabel.setMinimumHeight(40)
        fxlabel.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignRight)

        return fxlabel