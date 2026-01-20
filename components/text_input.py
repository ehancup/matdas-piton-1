from PyQt6.QtWidgets import QLineEdit, QLabel
from PyQt6.QtCore import Qt


class TextInput(QLineEdit):
    def __init__(self, label, placeholder="", parent=None):
        super().__init__(parent)

        self.label_text = label
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(44)

        self.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #e5e7eb;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 15px;
            }

            QLineEdit:focus {
                border-color: #4f46e5;
                background-color: #fefefe;
            }

            QLineEdit:hover {
                border-color: #c7d2fe;
            }
        """)

    def getLabel(self):
        label = QLabel(self.label_text)
        label.setMinimumHeight(44)
        label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight
        )

        label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: 600;
                color: #374151;
                padding-right: 8px;
            }
        """)

        return label
