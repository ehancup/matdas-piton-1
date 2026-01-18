import sympy as sp
from PyQt6.QtWidgets import (
    QWidget, QLabel,  QVBoxLayout, QFormLayout, QMessageBox, 
)

from components.label_title import LabelTitle
from components.button import Button
from components.text_input import TextInput


class InversPage(QWidget):
    def __init__(self):
        super().__init__()

        title = LabelTitle("Fungsi Invers")

        self.fungsi_awal = TextInput("f(x) = ", "Masukkan fungsi f(x)")

        self.save_btn = Button("hitung")

        form_layout = QFormLayout()
        form_layout.addRow(self.fungsi_awal.getLabel(), self.fungsi_awal)

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
        val = self.fungsi_awal.text()

        if not val:
            QMessageBox.warning(self, "Error", "fungsi wajib diisi!")
            return
        
        try:
            x, y = sp.symbols('x y')

            f = sp.sympify(val, locals={'sqrt': sp.sqrt})

            eq = f.subs(x, y)
            inverse = sp.solve(eq - x, y)

            if not inverse:
                raise ValueError("Tidak ada invers")
            
            inverse[0] = str(inverse[0]).replace("sqrt", "√")
            inverse[0] = str(inverse[0]).replace("**", "^")
            inverse[0] = str(inverse[0]).replace("*", "")

            result = f"f⁻¹(x) = {inverse[0]}"

            self.result_label.setText(result)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fungsi tidak valid:\n{e}")
