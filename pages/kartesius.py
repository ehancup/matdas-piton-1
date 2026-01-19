import sympy as sp
from PyQt6.QtWidgets import (
    QWidget, QLabel,  QVBoxLayout, QFormLayout, QMessageBox, 
)

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput


class KoordinatKartesiusPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Polar -> Kartesius")
        self.radiant = TextInput("r = ", "Masukkan radiant")
        self.theta = TextInput("θ = ", "Masukkan theta")

        self.save_btn = Button("hitung")

        form_layout = QFormLayout()
        form_layout.addRow(self.radiant.getLabel(), self.radiant)
        form_layout.addRow(self.theta.getLabel(), self.theta)

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
        nilair = self.radiant.text()
        nilaitheta = self.theta.text()

        if not nilair or not nilaitheta:
            QMessageBox.warning(self, "Error", "r dan theta wajib diisi!")
            return
        
        try:
            nilair = sp.sympify(nilair, locals={'sqrt': sp.sqrt})
            nilaitheta = sp.sympify(nilaitheta, locals={'sqrt': sp.sqrt})
            x= nilair * sp.cos(nilaitheta*sp.pi/180)
            y= nilair * sp.sin(nilaitheta*sp.pi/180)

            x=str(x).replace("sqrt", "√").replace("*", "")
            y=str(y).replace("sqrt", "√").replace("*", "")
            self.result_label.setText(f"x = {x}\ny = {y}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
