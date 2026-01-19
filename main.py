from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget,
    QStackedWidget, QHBoxLayout
)

# components
from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput

# pages
from pages.invers import InversPage
from pages.komposisi import KomposisiPage
from pages.domain import DomainPage
from pages.polar import KoordinatPolarPage
from pages.range import RangePage
from pages.kartesius import KoordinatKartesiusPage
from pages.turunan import TurunanPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tugas Matdas Gacor")
        self.resize(700, 400)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.addItem("Fungsi Invers")
        self.sidebar.addItem("Fungsi Komposisi")
        self.sidebar.addItem("Domain dan Range") 
        self.sidebar.addItem("Koordinat Polar")
        self.sidebar.addItem("Koordinat Kartesius")
        self.sidebar.addItem("Turunan Fungsi")
        self.sidebar.setFixedWidth(150)

        # Pages
        self.stack = QStackedWidget()
        self.stack.addWidget(InversPage())
        self.stack.addWidget(KomposisiPage())
        self.stack.addWidget(DomainPage())  
        self.stack.addWidget(KoordinatPolarPage())
        self.stack.addWidget(KoordinatKartesiusPage())
        self.stack.addWidget(TurunanPage())
        

        # Layout utama
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Connect sidebar ke stacked widget
        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.sidebar.setCurrentRow(0)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
