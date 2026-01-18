
import re
import sympy as sp
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFormLayout, QMessageBox

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput

class RangePage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Hitung Range Fungsi")

        self.fx = TextInput("f(x) = ", "Masukkan fungsi f(x)")

        self.save_btn = Button("Hitung Range")

        form_layout = QFormLayout()
        form_layout.addRow(self.fx.getLabel(), self.fx)

        self.hasil = QLabel("Range :")
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

        self.save_btn.clicked.connect(self.hitung_range)

    def preprocess_input(self, expr: str) -> str:
        """
        Perbaiki input agar bisa diparse SymPy:
        - x2 -> x**2
        - 3x -> 3*x
        """
        expr = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', expr)  
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)   
        return expr

    def hitung_range(self):
        fx = self.fx.text()

        if not fx:
            QMessageBox.warning(self, "Error", "f(x) wajib diisi!")
            return
        
        try:
            x = sp.symbols('x', real=True)

            fx = self.preprocess_input(fx)

            f = sp.sympify(fx, locals={
                'sqrt': sp.sqrt,
                'sin': sp.sin,
                'cos': sp.cos,
                'tan': sp.tan,
                'exp': sp.exp,
                'log': sp.log
            })

            domain = sp.calculus.util.continuous_domain(f, x, sp.S.Reals)

            if domain.is_EmptySet:
                raise ValueError("Domain fungsi kosong, tidak bisa hitung range.")

            f_prime = sp.diff(f, x)
            critical_points = sp.solve(f_prime, x, domain=domain)

            test_points = []

            test_points += critical_points

            if domain.start.is_finite:
                test_points.append(domain.start)
            if domain.end.is_finite:
                test_points.append(domain.end)

            values = []
            for pt in test_points:
                try:
                    val = f.subs(x, pt).evalf()
                    if val.is_real:
                        values.append(val)
                except:
                    continue

            min_val = min(values) if values else -sp.oo
            max_val = max(values) if values else sp.oo

            if domain.start.is_infinite:
                min_val = min_val  
            if domain.end.is_infinite:
                max_val = max_val  

            self.result_label.setText(f"[{min_val}, {max_val}]")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid atau tidak bisa dihitung:\n{e}")
