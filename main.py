from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget,
    QStackedWidget,QHBoxLayout
)

# components
from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput

# pages
from pages.invers import InversPage
from pages.komposisi import KomposisiPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tugas matdas gacor")
        self.resize(700, 400)

        self.sidebar = QListWidget()
        self.sidebar.addItem("Fungsi Invers")
        self.sidebar.addItem("Fungsi Komposisi")
        self.sidebar.setFixedWidth(150)

        # Pages
        self.stack = QStackedWidget()
        self.stack.addWidget(InversPage())
        self.stack.addWidget(KomposisiPage())

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.sidebar.setCurrentRow(0)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
