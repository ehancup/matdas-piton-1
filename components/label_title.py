from PyQt6.QtWidgets import QLabel


class LabelTitle(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 700;
                color: #1f2937;
                margin-bottom: 24px;
            }
        """)
