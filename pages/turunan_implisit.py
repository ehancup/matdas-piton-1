import sympy as sp
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFormLayout, QMessageBox,
)

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput
from lib.preinput import preprocess_input as pri
import numpy as np
import matplotlib.pyplot as plt

from lib.valid import is_valid_input


class TurunanImplisitPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Fungsi Turunan Implisit")
        self.fungsi_awal = TextInput("0 = ", "Masukkan fungsi f = 0")

        self.save_btn = Button("Hitung")

        form_layout = QFormLayout()
        form_layout.addRow(self.fungsi_awal.getLabel(), self.fungsi_awal)

        self.hasil = QLabel("Hasil:")
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
            QMessageBox.warning(self, "Error", "Fungsi wajib diisi!")
            return

        if not is_valid_input(val):
            QMessageBox.warning(self, "Error", "Input hanya boleh mengandung huruf x dan y saja!")
            return

        try:
            x, y = sp.symbols('x y')

            # Konversi string input ke objek sympy
            f = sp.sympify(val, locals={'sqrt': sp.sqrt })

            # Hitung turunan implisit
            dydx = -sp.diff(f, x) / sp.diff(f, y)

            # Buat fungsi numerik untuk plotting
            F_func = sp.lambdify((x, y), f, "numpy")

            # Grid untuk contour plot
            xx = np.linspace(-5, 5, 400)
            yy = np.linspace(-5, 5, 400)
            X, Y = np.meshgrid(xx, yy)
            Z = F_func(X, Y)

            # Tampilkan kurva implisit
            plt.figure(figsize=(7,6))
            plt.contour(X, Y, Z, levels=[0], colors='blue')
            plt.title(f'Kurva implisit: {val.replace("**", "^").replace("*", "")}\nTurunan implisit: dy/dx = {str(dydx).replace("sqrt", "√").replace("**", "^").replace("*", "")}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.show()

            # Tampilkan turunan implisit di label
            dydx_str = str(dydx).replace("sqrt", "√").replace("**", "^").replace("*", "")
            self.result_label.setText(f"dydx = {dydx_str}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
