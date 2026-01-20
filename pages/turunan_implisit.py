import sympy as sp
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput
from lib.preinput import preprocess_input as pri
import numpy as np
import matplotlib.pyplot as plt

class TurunanImplisitPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Fungsi Turunan Implisit")

        self.fungsi_awal = TextInput("f(x, y) =", "Masukkan fungsi f(x, y)")

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

        # Label input
        label_fx = QLabel("f(x, y) =")
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
            x, y = sp.symbols('x y')
            f = sp.sympify(val, locals={'sqrt': sp.sqrt})

            # Turunan implisit
            dydx = -sp.diff(f, x) / sp.diff(f, y)
            dydx_str = str(dydx).replace("sqrt", "√").replace("**", "^").replace("*", "")

            # Buat grid untuk grafik
            xx = np.linspace(-3, 3, 400)
            yy = np.linspace(-3, 3, 400)
            X, Y = np.meshgrid(xx, yy)
            F_func = sp.lambdify((x, y), f, "numpy")
            Z = F_func(X, Y)

            # Plot contour f(x,y) = 0
            plt.figure()
            plt.contour(X, Y, Z, levels=[0], colors='blue')
            plt.title(f'Grafik turunan implisit dydx')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)
            plt.show()

            self.result_label.setText(f"dydx = {dydx_str}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
