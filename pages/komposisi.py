import sympy as sp
import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
import lib.preinput as pri
from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput

class KomposisiPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Fungsi Komposisi")

        self.fx = TextInput("Masukkan fungsi f(x)")
        self.gx = TextInput("Masukkan fungsi g(x)")

        self.save_btn = Button("Hitung")
        self.save_btn.setMinimumHeight(44)
        self.save_btn.setFixedWidth(140)
        self.save_btn.setStyleSheet("background-color: #4f46e5; color: white; font-size: 14px; border-radius: 8px;")

        # Label f(x) dan g(x)
        label_fx = QLabel("f(x) =")
        label_fx.setMinimumHeight(44)
        label_fx.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        label_fx.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151;")

        label_gx = QLabel("g(x) =")
        label_gx.setMinimumHeight(44)
        label_gx.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        label_gx.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151;")

        # Layout input f(x) + button
        fx_layout = QHBoxLayout()
        fx_layout.setSpacing(10)
        fx_layout.addWidget(label_fx)
        fx_layout.addWidget(self.fx, 3)
        fx_layout.addWidget(self.save_btn, 1)

        # Layout input g(x)
        gx_layout = QHBoxLayout()
        gx_layout.setSpacing(10)
        gx_layout.addWidget(label_gx)
        gx_layout.addWidget(self.gx, 3)
        gx_layout.addStretch()

        # Hasil
        self.hasil = QLabel("Hasil :")
        self.hasil.setStyleSheet("font-size: 18px; font-weight: 700; color: #111827; margin-top: 10px; margin-bottom: 5px;")
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 24px; font-weight: 800; color: #1E40AF; margin-bottom: 20px;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addWidget(title)
        main_layout.addLayout(fx_layout)
        main_layout.addLayout(gx_layout)
        main_layout.addWidget(self.hasil)
        main_layout.addWidget(self.result_label)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.save_btn.clicked.connect(self.hitung)

    def hitung(self):
        plt.close('all')
        fx = pri.preprocess_input(self.fx.text()).replace("^", "**")
        gx = pri.preprocess_input(self.gx.text()).replace("^", "**")

        if not fx or not gx:
            QMessageBox.warning(self, "Error", "f(x) dan g(x) wajib diisi!")
            return

        try:
            x = sp.symbols('x')
            f = sp.sympify(fx, locals={'sqrt': sp.sqrt})
            g = sp.sympify(gx, locals={'sqrt': sp.sqrt})

            compose_fg = sp.compose(f, g)
            compose_gf = sp.compose(g, f)

            # Plot grafik
            f_func = sp.lambdify(x, f, "numpy")
            g_func = sp.lambdify(x, g, "numpy")
            fog_func = sp.lambdify(x, compose_fg, "numpy")
            gof_func = sp.lambdify(x, compose_gf, "numpy")
            x_vals = np.linspace(-10, 10, 500)

            plt.figure()
            plt.plot(x_vals, f_func(x_vals), label='f(x)')
            plt.plot(x_vals, g_func(x_vals), label='g(x)')
            plt.plot(x_vals, fog_func(x_vals), label='(f ∘ g)(x)', linestyle='--')
            plt.plot(x_vals, gof_func(x_vals), label='(g ∘ f)(x)', linestyle='--')
            plt.title('Grafik Fungsi Komposisi')
            plt.xlabel('x')
            plt.ylabel('f(x)')
            plt.grid(True)
            plt.legend(fontsize=10, frameon=True, shadow=True, loc="best")
            plt.show()

            # Tampilkan hasil string
            compose_fg_str = str(compose_fg).replace("sqrt", "√").replace("**", "^").replace("*", "")
            compose_gf_str = str(compose_gf).replace("sqrt", "√").replace("**", "^").replace("*", "")
            result = f"(f ∘ g)(x) = {compose_fg_str}\n(g ∘ f)(x) = {compose_gf_str}"
            self.result_label.setText(result)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
