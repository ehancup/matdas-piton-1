from PyQt6.QtWidgets import QLabel

class LabelTitle(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")