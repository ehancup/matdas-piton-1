import sympy as sp
from PyQt6.QtWidgets import (
    QWidget, QLabel,  QVBoxLayout, QFormLayout, QMessageBox, 
)

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput
from lib.preinput import preprocess_input as pri
import numpy as np
import matplotlib.pyplot as plt


class TurunanPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Fungsi Turunan")

        self.fungsi_awal = TextInput("f(x) = ", "Masukkan fungsi f(x)")

        self.save_btn = Button("hitung")

        form_layout = QFormLayout()
        form_layout.addRow(self.fungsi_awal.getLabel(), self.fungsi_awal)

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
        plt.close('all')
        val = self.fungsi_awal.text()
        val = pri(val).replace("^", "**")

        if not val:
            QMessageBox.warning(self, "Error", "fungsi wajib diisi!")
            return
        
        try:
            x = sp.symbols('x')

            f = sp.sympify(val, locals={'sqrt': sp.sqrt })
            
            derivative = sp.diff(f, x)
            print(derivative)
            f_origin = sp.lambdify(x, f, "numpy")
            x_value = np.linspace(-10, 10, 500)
            y_origin = f_origin(x_value)
            
            y_derivative = sp.lambdify(x, derivative, "numpy")
            y_deriv_value = y_derivative(x_value)
            
            derivative = str(derivative).replace("sqrt", "√").replace("**", "^").replace("*", "")
            plt.figure()
            plt.plot(x_value, y_origin, label='f(x)')
            plt.plot(x_value, y_deriv_value, label="f'(x)", linestyle='--')
            plt.title(f'Grafik turunan f\' (x) = {derivative}') # Judul grafik
            plt.xlabel('x') # Label sumbu x
            plt.ylabel('f(x)') # Label sumbu y
            
            plt.grid(True)
            plt.legend(
                fontsize=10,
                frameon=True,
                shadow=True,
                loc="best"
            )
            plt.show()

            self.result_label.setText(f"f'(x) = {derivative}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
