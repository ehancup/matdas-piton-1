import sympy as sp
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QMessageBox
from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput
from PyQt6.QtCore import Qt

class DomainPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Hitung Domain dan Range")

        self.fx = TextInput("Masukkan fungsi f(x)")

        self.save_btn = Button("Hitung Domain")
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
        input_btn_layout.addWidget(self.fx, 3)
        input_btn_layout.addWidget(self.save_btn, 1)

        self.hasil = QLabel("Domain :")
        self.hasil.setStyleSheet("font-size: 18px; font-weight: 700; color: #111827; margin-top: 10px; margin-bottom: 5px;")
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 24px; font-weight: 800; color: #1E40AF; margin-bottom: 20px;")

        self.hasil_range = QLabel("Range :")
        self.hasil_range.setStyleSheet("font-size: 18px; font-weight: 700; color: #111827; margin-top: 10px; margin-bottom: 5px;")
        self.range_result = QLabel("")
        self.range_result.setStyleSheet("font-size: 24px; font-weight: 800; color: #1E40AF; margin-bottom: 20px;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(25)
        main_layout.addWidget(title)
        main_layout.addLayout(input_btn_layout)
        main_layout.addWidget(self.hasil)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.hasil_range)
        main_layout.addWidget(self.range_result)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.save_btn.clicked.connect(self.hitung_domain)

    def hitung_domain(self):
        fx = self.fx.text()
        if not fx:
            QMessageBox.warning(self, "Error", "f(x) wajib diisi!")
            return
        try:
            x = sp.symbols('x', real=True)
            f = sp.sympify(fx, locals={'sqrt': sp.sqrt, 'x': x})
            domain = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)
            range_ = sp.calculus.util.function_range(f, x, sp.S.Reals)
            self.result_label.setText("{ x | x ∈ ℝ}" if domain == sp.S.Reals else f"{{ x | {self.domain_to_text(domain)}, x ∈ ℝ }}")
            self.range_result.setText("{ y | y ∈ ℝ}" if range_ == sp.S.Reals else f"{{ y | {self.domain_to_text(range_).replace('x', 'y')}, y ∈ ℝ }}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")

    def domain_to_text(self, domain):
        if isinstance(domain, sp.Interval):
            a, b = domain.start, domain.end
