import sympy as sp
from PyQt6.QtWidgets import (
    QWidget, QLabel,  QVBoxLayout, QFormLayout, QMessageBox, 
)

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput


class KomposisiPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Fungsi Komposisi")

        self.fx = TextInput("f(x) = ", "Masukkan fungsi f(x)")
        self.gx = TextInput("g(x) = ", "Masukkan fungsi g(x)")

        self.save_btn = Button("hitung")

        form_layout = QFormLayout()
        form_layout.addRow(self.fx.getLabel(), self.fx)
        form_layout.addRow(self.gx.getLabel(), self.gx)

        self.hasil = QLabel("hasil :")
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
        fx = self.fx.text()
        gx = self.gx.text()

        if not fx or not gx:
            QMessageBox.warning(self, "Error", "f(x) dan g(x) wajib diisi!")
            return
        
        try:
            x = sp.symbols('x')

            f = sp.sympify(fx, locals={'sqrt': sp.sqrt})
            g = sp.sympify(gx, locals={'sqrt': sp.sqrt})

            # eq = f.subs(x, y)
            compose_fg = sp.compose(f, g)
            compose_gf = sp.compose(g, f)

            # if not inverse:
            #     raise ValueError("Tidak ada invers")
            
            compose_fg = str(compose_fg).replace("sqrt", "√")
            compose_fg = str(compose_fg).replace("**", "^")
            compose_fg = str(compose_fg).replace("*", "")

            compose_gf = str(compose_gf).replace("sqrt", "√")
            compose_gf = str(compose_gf).replace("**", "^")
            compose_gf = str(compose_gf).replace("*", "")

            result = f"(f ∘ g)(x) = {compose_fg}\n(g ∘ f)(x) = {compose_gf}"

            self.result_label.setText(result)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
