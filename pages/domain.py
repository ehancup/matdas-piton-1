import sympy as sp
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QMessageBox

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput

class DomainPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Hitung Fungsi Domain")

        self.fx = TextInput("f(x) = ", "Masukkan fungsi f(x)")

        self.save_btn = Button("Hitung Domain")

        form_layout = QFormLayout()
        form_layout.addRow(self.fx.getLabel(), self.fx)

        self.hasil = QLabel("Domain :")
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

        self.save_btn.clicked.connect(self.hitung_domain)

    def hitung_domain(self):
        fx = self.fx.text()

        if not fx:
            QMessageBox.warning(self, "Error", "f(x) wajib diisi!")
            return
        
        try:
            x = sp.symbols('x', real=True)

            f = sp.sympify(fx, locals={'sqrt': sp.sqrt})

            domain = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)

            domain_str = str(domain).replace("Interval", "").replace("Union", "∪")
            domain_str = domain_str.replace("(", "(").replace(")", ")")

            self.result_label.setText(domain_str)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
