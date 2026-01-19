import sympy as sp
from PyQt6.QtWidgets import (
    QWidget, QLabel,  QVBoxLayout, QFormLayout, QMessageBox, 
)

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput

import re
import numpy as np
import matplotlib.pyplot as plt
import lib.preinput as pri


class InversPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Fungsi Invers")

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
        val = self.fungsi_awal.text()
        val = pri.preprocess_input(val)

        if not val:
            QMessageBox.warning(self, "Error", "fungsi wajib diisi!")
            return
        
        try:
            plt.close('all')
            x, y = sp.symbols('x y')

            f = sp.sympify(val, locals={'sqrt': sp.sqrt})

            eq = f.subs(x, y)
            inverse = sp.solve(eq - x, y)
            
            f_origin = sp.lambdify(x, f, "numpy")
            x_value = np.linspace(-10, 10, 500)
            y_origin = f_origin(x_value)
            
            y_inverse = sp.lambdify(x, inverse[0], "numpy")
            y_inv_value = y_inverse(x_value)
            
            plt.figure()
            plt.plot(x_value, y_origin, label='f(x)')
            plt.plot(x_value, y_inv_value, label='f⁻¹(x)', linestyle='--')
            plt.title('Grafik Fungsi f(x) = x^2') # Judul grafik
            plt.xlabel('x') # Label sumbu x
            plt.ylabel('f(x)') # Label sumbu y
            
            plt.grid(True)
            if not inverse:
                raise ValueError("Tidak ada invers")
            
            plt.show()
            inverse[0] = str(inverse[0]).replace("sqrt", "√")
            inverse[0] = str(inverse[0]).replace("**", "^")
            # table = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
            # inverse[0] = inverse[0].translate(table)
            inverse[0] = str(inverse[0]).replace("*", "")

            result = f"f⁻¹(x) = {inverse[0]}"

            self.result_label.setText(result)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
