import sympy as sp
from PyQt6.QtWidgets import (
    QWidget, QLabel,  QVBoxLayout, QFormLayout, QMessageBox, QHBoxLayout, QPushButton, QStackedWidget
)

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput
from pages.kartesius import KoordinatKartesiusPage

class CobaCoba(QWidget):
    def __init__(self):
        super().__init__()
        
        title = LabelTitle("Koordinat Polar & Kartesius")
        
        self.button_polar = QPushButton("Kartesius -> Polar")
        self.button_polar.setCheckable(True)
        self.button_polar.setMinimumHeight(30)
        self.button_cartesian = QPushButton("Polar -> Kartesius")
        self.button_cartesian.setMinimumHeight(30)
        # self.button_cartesian.setStyleSheet("border: 1px solid white; border-radius: 5px; padding: 3px; text-color: black; color: lightgray;")
        self.button_cartesian.setCheckable(True)
        
        self.button_polar.clicked.connect(lambda: self.navigate(0, self.button_polar))
        self.button_cartesian.clicked.connect(lambda: self.navigate(1, self.button_cartesian))
        
        row_button = QHBoxLayout()
        
        row_button.addWidget(self.button_polar)
        row_button.addWidget(self.button_cartesian)
        
        main_layout = QVBoxLayout()

        self.stack = QStackedWidget()
        self.stack.addWidget(KoordinatPolarPage())
        self.stack.addWidget(KoordinatKartesiusPage())

        main_layout.addWidget(title)
        main_layout.addLayout(row_button)
        main_layout.addWidget(self.stack)
        main_layout.addStretch()
        
        

        self.setLayout(main_layout)
        
        self.navigate(0, self.button_polar)
    
    def navigate(self, index, button):
        self.stack.setCurrentIndex(index)

        self.button_polar.setChecked(False)
        self.button_cartesian.setChecked(False)

        button.setChecked(True)


class KoordinatPolarPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Kartesius -> Polar")

        self.titikx = TextInput("x = ", "Masukkan x")
        self.titiky = TextInput("y = ", "Masukkan y")

        self.save_btn = Button("hitung")

        form_layout = QFormLayout()
        form_layout.addRow(self.titikx.getLabel(), self.titikx)
        form_layout.addRow(self.titiky.getLabel(), self.titiky)

        self.hasil = QLabel("hasil :")
        self.hasil.setStyleSheet("font-size: 18px; margin-bottom: 5px; margin-top: 10px;")
        
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.save_btn)
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
            r=sp.sqrt(nilaix**2 + nilaiy**2)
            theta=sp.atan2(nilaiy, nilaix)
            
            r=str(r).replace("sqrt", "√").replace("*", "")
            theta=str(theta).replace("sqrt", "√")
            theta=theta.replace("pi", "180")
            theta=str(eval(theta))
            self.result_label.setText(f"r = {r}\nθ = {theta}°")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
