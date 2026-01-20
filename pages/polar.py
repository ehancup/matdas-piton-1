import sympy as sp
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt
from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput
from pages.kartesius import KoordinatKartesiusPage

class CobaCoba(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Koordinat Polar & Kartesius")

        self.button_polar = Button("Kartesius -> Polar")
        self.button_polar.setCheckable(True)
        self.button_cartesian = Button("Polar -> Kartesius")
        self.button_cartesian.setCheckable(True)

        self.set_button_style(self.button_polar, active=False)
        self.set_button_style(self.button_cartesian, active=False)

        self.button_polar.clicked.connect(lambda: self.navigate(0, self.button_polar))
        self.button_cartesian.clicked.connect(lambda: self.navigate(1, self.button_cartesian))

        row_button = QHBoxLayout()
        row_button.setSpacing(10)
        row_button.addWidget(self.button_polar)
        row_button.addWidget(self.button_cartesian)

        self.stack = QStackedWidget()
        self.stack.addWidget(KoordinatPolarPage())
        self.stack.addWidget(KoordinatKartesiusPage())

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        main_layout.addWidget(title)
        main_layout.addLayout(row_button)
        main_layout.addWidget(self.stack)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.navigate(0, self.button_polar)

    def set_button_style(self, button, active=False):
        if active:
            button.setStyleSheet("""
                background-color: #4f46e5; 
                color: white; 
                font-size: 20px; 
                border-radius: 8px;
            """)
        else:
            button.setStyleSheet("""
                background-color: #e5e7eb; 
                color: #111827; 
                font-size: 20px; 
                border-radius: 8px;
            """)

    def navigate(self, index, button):
        self.stack.setCurrentIndex(index)

        # Reset semua tombol
        self.button_polar.setChecked(False)
        self.button_cartesian.setChecked(False)
        self.set_button_style(self.button_polar, active=False)
        self.set_button_style(self.button_cartesian, active=False)

        # Aktifkan tombol yang dipilih
        button.setChecked(True)
        self.set_button_style(button, active=True)


class KoordinatPolarPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Kartesius -> Polar")

        self.titikx = TextInput("Masukkan x")
        self.titiky = TextInput("Masukkan y")

        self.save_btn = Button("Hitung")
        self.save_btn.setMinimumHeight(44)
        self.save_btn.setFixedWidth(140)
        self.save_btn.setStyleSheet("background-color: #4f46e5; color: white; font-size: 14px; border-radius: 8px;")

        label_x = QLabel("x =")
        label_x.setMinimumHeight(44)
        label_x.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        label_x.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151;")

        label_y = QLabel("y =")
        label_y.setMinimumHeight(44)
        label_y.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        label_y.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151;")

        # Layout input + tombol
        x_layout = QHBoxLayout()
        x_layout.setSpacing(10)
        x_layout.addWidget(label_x)
        x_layout.addWidget(self.titikx, 3)
        x_layout.addWidget(self.save_btn, 1)

        y_layout = QHBoxLayout()
        y_layout.setSpacing(10)
        y_layout.addWidget(label_y)
        y_layout.addWidget(self.titiky, 3)
        y_layout.addStretch()

        self.hasil = QLabel("Hasil :")
        self.hasil.setStyleSheet("font-size: 18px; font-weight: 700; color: #111827; margin-top: 10px; margin-bottom: 5px;")
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 24px; font-weight: 800; color: #1E40AF; margin-bottom: 20px;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addWidget(title)
        main_layout.addLayout(x_layout)
        main_layout.addLayout(y_layout)
        main_layout.addWidget(self.hasil)
        main_layout.addWidget(self.result_label)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.save_btn.clicked.connect(self.hitung)

    def hitung(self):
        nilaix = self.titikx.text()
        nilaiy = self.titiky.text()

        if not nilaix or not nilaiy:
            QMessageBox.warning(self, "Error", "x dan y wajib diisi!")
            return
        
        try:
            nilaix = sp.sympify(nilaix, locals={'sqrt': sp.sqrt})
            nilaiy = sp.sympify(nilaiy, locals={'sqrt': sp.sqrt})
            r = sp.sqrt(nilaix**2 + nilaiy**2)
            theta = sp.atan2(nilaiy, nilaix)
            
            r_str = str(r).replace("sqrt", "√").replace("*", "")
            theta_str = str(theta).replace("sqrt", "√").replace("pi", "180")
            theta_str = str(eval(theta_str))

            self.result_label.setText(f"r = {r_str}\nθ = {theta_str}°")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
