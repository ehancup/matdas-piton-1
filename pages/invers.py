import sympy as sp
import numpy as np
import lib.preinput as pri
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox, QLineEdit
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl
from components.label_title import LabelTitle
from components.button import Button

mpl.rcParams["lines.antialiased"] = True
mpl.rcParams["path.simplify"] = True
mpl.rcParams["path.simplify_threshold"] = 0.1
mpl.rcParams["font.size"] = 10

class TextInput(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(44)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #e5e7eb;
                border-radius: 10px;
                padding-left: 8px;
                padding-top: 8px;
                padding-bottom: 8px;
                font-size: 15px;
            }
            QLineEdit:focus {
                border-color: #4f46e5;
                background-color: #fefefe;
            }
            QLineEdit:hover {
                border-color: #c7d2fe;
            }
        """)

class InversPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Fungsi Invers")
        self.fungsi_awal = TextInput("contoh: x^2, 2*x+1, sqrt(x)")
        self.save_btn = Button("Hitung Invers")
        self.save_btn.setMinimumHeight(44)
        self.save_btn.setFixedWidth(140)
        self.save_btn.setStyleSheet("background-color: #4f46e5; color: white; font-size: 14px; border-radius: 8px;")

        label_fx = QLabel("f(x) =")
        label_fx.setMinimumHeight(44)
        label_fx.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        label_fx.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151;")

        input_btn_layout = QHBoxLayout()
        input_btn_layout.setSpacing(10)
        input_btn_layout.addWidget(label_fx)
        input_btn_layout.addWidget(self.fungsi_awal, 3)
        input_btn_layout.addWidget(self.save_btn, 1)

        self.hasil = QLabel("Hasil")
        self.hasil.setStyleSheet("""
            font-size: 16px;
            font-weight: 700;
            color: #111827;
        """)

        self.result_label = QLabel("–")
        self.result_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 800;
            color: #1E40AF;
            margin-bottom: 20px;
            margin-top: -6px
        """)


        hasil_layout = QVBoxLayout()
        hasil_layout.addWidget(self.hasil)
        hasil_layout.addWidget(self.result_label)
        hasil_layout.addStretch()

        top_layout = QHBoxLayout()
        top_layout.setSpacing(40)
        top_layout.addLayout(input_btn_layout, 3)
        top_layout.addLayout(hasil_layout, 2)

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: white; border-radius: 12px;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)
        main_layout.addWidget(title)
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.canvas, 2)
        self.setLayout(main_layout)

        self.save_btn.clicked.connect(self.hitung)

    def hitung(self):
        val = pri.preprocess_input(self.fungsi_awal.text())
        if not val:
            QMessageBox.warning(self, "Error", "Fungsi wajib diisi!")
            return
        try:
            x, y = sp.symbols("x y")
            f = sp.sympify(val, locals={"sqrt": sp.sqrt})
            inverse = sp.solve(f.subs(x, y) - x, y)
            if not inverse:
                raise ValueError("Fungsi tidak memiliki invers")
            inv_expr = inverse[0]
            f_func = sp.lambdify(x, f, "numpy")
            inv_func = sp.lambdify(x, inv_expr, "numpy")
            x_vals = np.linspace(-10, 10, 3000)
            y_f = f_func(x_vals)
            y_inv = inv_func(x_vals)
            mask = np.isfinite(y_f) & np.isfinite(y_inv)
            x_vals = x_vals[mask]
            y_f = y_f[mask]
            y_inv = y_inv[mask]
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            color_f = "#2563EB"
            color_inv = "#D97706"
            color_yx = "#6B7280"
            ax.plot(x_vals, y_f, label="f(x)", color=color_f, linewidth=2.8)
            ax.plot(x_vals, y_inv, label="f⁻¹(x)", color=color_inv, linestyle="--", linewidth=2.8)
            ax.plot(x_vals, x_vals, linestyle=":", color=color_yx, linewidth=1.7, alpha=0.8, label="y = x")
            ax.scatter(x_vals[-1], y_f[-1], color=color_f, s=30, zorder=5)
            ax.scatter(x_vals[-1], y_inv[-1], color=color_inv, s=30, zorder=5)
            ax.set_facecolor("#F9FAFB")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_linewidth(1.2)
            ax.spines["bottom"].set_linewidth(1.2)
            ax.set_title(f"Grafik Fungsi dan Invers\nf(x) = {val}", fontsize=12, weight="bold", color="#111827")
            ax.set_xlabel("x", fontsize=11, weight="medium", color="#111827")
            ax.set_ylabel("y", fontsize=11, weight="medium", color="#111827")
            ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.4)
            ax.legend(frameon=False, fontsize=10)
            self.figure.tight_layout()
            self.canvas.draw()
            inv_str = str(inv_expr).replace("sqrt", "√").replace("**", "^").replace("*", "")
            self.result_label.setText(f"f⁻¹(x) = {inv_str}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid atau tidak memiliki invers.\n\n{e}")
