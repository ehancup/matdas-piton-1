import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QListWidget,
    QStackedWidget, QHBoxLayout
)
from PyQt6.QtCore import Qt

# pages
from pages.invers import InversPage
from pages.komposisi import KomposisiPage
from pages.domain import DomainPage
from pages.polar import CobaCoba
from pages.kartesius import KoordinatKartesiusPage
from pages.turunan import TurunanPage
from pages.turunan_implisit import TurunanImplisitPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tugas Matdas Gacor")
        self.resize(900, 500)

        # =========================
        # SIDEBAR
        # =========================
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)

        menu_items = [
            "Fungsi Invers",
            "Fungsi Komposisi",
            "Domain dan Range",
            "Polar & Kartesius",
            "Turunan",
            "Turunan Implisit",
        ]

        self.sidebar.addItems(menu_items)

        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                border: none;
                font-size: 14px;
                outline: 0;
            }

            QListWidget::item {
                padding: 14px 18px;
                margin: 6px;
                border-radius: 10px;
            }

            QListWidget::item:selected {
                background-color: #4f46e5;
                color: white;
            }

            QListWidget::item:hover {
                background-color: #6366f1;
            }
        """)

        self.sidebar.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sidebar.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.sidebar.setCurrentRow(0)

        # =========================
        # STACKED PAGES
        # =========================
        self.stack = QStackedWidget()
        self.stack.addWidget(InversPage())
        self.stack.addWidget(KomposisiPage())
        self.stack.addWidget(DomainPage())
        self.stack.addWidget(CobaCoba())
        self.stack.addWidget(TurunanPage())
        self.stack.addWidget(TurunanImplisitPage())

        # =========================
        # LAYOUT UTAMA
        # =========================
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # =========================
        # CONNECT
        # =========================
        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Global style (opsional)
    app.setStyleSheet("""
        QWidget {
            background-color: #f8fafc;
            font-family: Segoe UI;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
