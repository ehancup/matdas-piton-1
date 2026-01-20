from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt


class Button(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self.setMinimumHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: white;
                font-size: 16px;
                font-weight: 600;
                border: none;
                border-radius: 12px;
                padding: 10px 20px;
                margin-top: 20px;
            }

            QPushButton:hover {
                background-color: #6366f1;
            }

            QPushButton:pressed {
                background-color: #4338ca;
            }

            QPushButton:disabled {
                background-color: #a5b4fc;
                color: #f1f5f9;
            }
        """)
