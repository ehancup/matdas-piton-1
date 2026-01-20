import sympy as sp
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
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

        self.save_btn = Button("Hitung Turunan")
        self.save_btn.setMinimumHeight(44)
        self.save_btn.setFixedWidth(160)
        self.save_btn.setStyleSheet("""
            background-color: #4f46e5;
            color: white;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
        """)

        # Label untuk input
        label_fx = QLabel("f(x) =")
        label_fx.setMinimumHeight(44)
        label_fx.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        label_fx.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151;")

        # Layout input + tombol
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        input_layout.addWidget(label_fx)
        input_layout.addWidget(self.fungsi_awal, 3)
        input_layout.addWidget(self.save_btn, 1)

        # Hasil
        self.hasil = QLabel("Hasil :")
        self.hasil.setStyleSheet("font-size: 18px; font-weight: 700; color: #111827; margin-top: 10px; margin-bottom: 5px;")
        self.result_label = QLabel("–")
        self.result_label.setStyleSheet("font-size: 24px; font-weight: 800; color: #1E40AF; margin-bottom: 20px;")

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addWidget(title)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.hasil)
        main_layout.addWidget(self.result_label)
        main_layout.addStretch()

        self.setLayout(main_layout)

        self.save_btn.clicked.connect(self.hitung)

    def hitung(self):
        plt.close('all')
        val = pri(self.fungsi_awal.text()).replace("^", "**")

        if not val:
            QMessageBox.warning(self, "Error", "Fungsi wajib diisi!")
            return
        
        try:
            x = sp.symbols('x')
            f = sp.sympify(val, locals={'sqrt': sp.sqrt})
            
            derivative = sp.diff(f, x)
            derivative_str = str(derivative).replace("sqrt", "√").replace("**", "^").replace("*", "")

            f_func = sp.lambdify(x, f, "numpy")
            deriv_func = sp.lambdify(x, derivative, "numpy")
            x_vals = np.linspace(-10, 10, 500)
            y_vals = f_func(x_vals)
            y_deriv_vals = deriv_func(x_vals)

            plt.figure()
            plt.plot(x_vals, y_vals, label='f(x)')
            plt.plot(x_vals, y_deriv_vals, label="f'(x)", linestyle='--')
            plt.title(f'Grafik f(x) dan f\'(x)') 
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.legend(fontsize=10, frameon=True, shadow=True, loc="best")
            plt.show()

            self.result_label.setText(f"f'(x) = {derivative_str}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
