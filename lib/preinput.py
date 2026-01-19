import re

def preprocess_input(expr: str) -> str:
        """
        Perbaiki input agar bisa diparse SymPy:
        - x2 -> x**2
        - 3x -> 3*x
        """
        expr = re.sub(r'([a-zA-Z])(\d+)', r'\1**\2', expr)  
        expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)   
        return expr