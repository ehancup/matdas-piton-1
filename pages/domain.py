import sympy as sp
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QMessageBox

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput
from lib.valid import is_valid_input
import lib.preinput as pri

class DomainPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Hitung Domain dan Range")

        self.fx = TextInput("f(x) = ", "Masukkan fungsi f(x)")

        self.save_btn = Button("Hitung Domain")

        form_layout = QFormLayout()
        form_layout.addRow(self.fx.getLabel(), self.fx)

        self.hasil = QLabel("Domain :")
        self.hasil.setStyleSheet("font-size: 18px; margin-bottom: 5px; margin-top: 10px;")
        
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        self.hasil_range = QLabel("Range :")
        self.hasil_range.setStyleSheet("font-size: 18px; margin-bottom: 5px; margin-top: 10px;")
        self.range_result = QLabel("")
        self.range_result.setStyleSheet("font-size: 24px; font-weight: bold;")

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.save_btn)
        main_layout.addWidget(self.hasil)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.hasil_range)
        main_layout.addWidget(self.range_result)
        main_layout.addStretch()    

        self.setLayout(main_layout)

        self.save_btn.clicked.connect(self.hitung_domain)

    def hitung_domain(self):
        fx = self.fx.text()
        fx = pri.preprocess_input(fx)

        if not fx:
            QMessageBox.warning(self, "Error", "f(x) wajib diisi!")
            return
        
        if not is_valid_input(fx):
            QMessageBox.warning(self, "Error", "Input hanya boleh mengandung huruf x dan y saja!")
            return
        
        try:
            x = sp.symbols('x', real=True)

            f = sp.sympify(fx, locals={'sqrt': sp.sqrt, 'x': x})

            domain = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)
            range_ = sp.calculus.util.function_range(f, x, sp.S.Reals)
            print(type(domain))

            # domain_str = str(domain).replace("Interval", "").replace("Union", "∪")
            # domain_str = domain_str.replace("(", "(").replace(")", ")")
            

            self.result_label.setText("{ x | x ∈ ℝ}" if domain == sp.S.Reals else f"{{ x | {self.domain_to_text(domain)}, x ∈ ℝ }}")
            self.range_result.setText("{ y | y ∈ ℝ}" if range_ == sp.S.Reals else f"{{ y | {self.domain_to_text(range_).replace('x', 'y')}, y ∈ ℝ }}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")

    def domain_to_text(self, domain):
        # if domain == sp.S.Reals:
        #     return "{ x | x ∈ ℝ}"

        if isinstance(domain, sp.Interval):
            a, b = domain.start, domain.end

            left = "<=" if not domain.left_open else "<"
            right = "<=" if not domain.right_open else "<"
            a_str = "-∞" if a == -sp.oo else str(a)
            b_str = "∞" if b == sp.oo else str(b)
            
            print(a_str+left)
            print(right+b_str)

            return f"{"" if (a_str+left)=="-∞<" else (a_str+" "+left+" ")}x{"" if (right+b_str)=="<∞" else (" "+right+" "+b_str)}"

        if isinstance(domain, sp.Union):
            print(domain)
            parts = [self.domain_to_text(arg) for arg in domain.args]
            s = [i.split() for i in parts]
            print(s)
            return " atau ".join(parts)

        return str(domain)