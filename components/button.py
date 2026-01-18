from PyQt6.QtWidgets import QPushButton

class Button(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(80)
        self.setStyleSheet("font-size: 18px; margin-top: 20px; font-weight: bold;")