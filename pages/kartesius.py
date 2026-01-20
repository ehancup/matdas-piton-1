import sympy as sp
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput

class KoordinatKartesiusPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Polar -> Kartesius")

        self.r_input = TextInput("Masukkan r")
        self.theta_input = TextInput("Masukkan θ")

        self.save_btn = Button("Hitung")
        self.save_btn.setMinimumHeight(44)
        self.save_btn.setFixedWidth(140)
        self.save_btn.setStyleSheet("""
            background-color: #4f46e5;
            color: white;
            font-size: 14px;
            border-radius: 8px;
        """)

        label_r = QLabel("r =")
        label_r.setMinimumHeight(44)
        label_r.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        label_r.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151;")

        label_theta = QLabel("θ =")
        label_theta.setMinimumHeight(44)
        label_theta.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        label_theta.setStyleSheet("font-size: 16px; font-weight: bold; color: #374151;")

        # Layout input + tombol
        r_layout = QHBoxLayout()
        r_layout.setSpacing(10)
        r_layout.addWidget(label_r)
        r_layout.addWidget(self.r_input, 3)
        r_layout.addWidget(self.save_btn, 1)

        theta_layout = QHBoxLayout()
        theta_layout.setSpacing(10)
        theta_layout.addWidget(label_theta)
        theta_layout.addWidget(self.theta_input, 3)
        theta_layout.addStretch()

        self.hasil = QLabel("Hasil :")
        self.hasil.setStyleSheet("""
            font-size: 18px;
            font-weight: 700;
            color: #111827;
            margin-top: 10px;
            margin-bottom: 5px;
        """)
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 800;
            color: #1E40AF;
            margin-bottom: 20px;
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addWidget(title)
        main_layout.addLayout(r_layout)
        main_layout.addLayout(theta_layout)
        main_layout.addWidget(self.hasil)
        main_layout.addWidget(self.result_label)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.save_btn.clicked.connect(self.hitung)

    def hitung(self):
        r_val = self.r_input.text()
        theta_val = self.theta_input.text()

        if not r_val or not theta_val:
            QMessageBox.warning(self, "Error", "r dan θ wajib diisi!")
            return
        
        try:
            r_val = sp.sympify(r_val, locals={'sqrt': sp.sqrt})
            theta_val = sp.sympify(theta_val, locals={'pi': sp.pi})

            x = r_val * sp.cos(theta_val * sp.pi / 180)
            y = r_val * sp.sin(theta_val * sp.pi / 180)

            x_str = str(x).replace("sqrt", "√").replace("*", "")
            y_str = str(y).replace("sqrt", "√").replace("*", "")

            self.result_label.setText(f"x = {x_str}\ny = {y_str}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
