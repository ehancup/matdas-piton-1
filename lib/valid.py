import re

def is_valid_input(expr: str) -> bool:
    # Cari huruf apa saja (case insensitive)
    # Jika ada huruf selain x dan y, return False
    letters = re.findall(r'[a-zA-Z]', expr)
    for letter in letters:
        if letter.lower() not in ('x', 'y', 's', 'q', 'r', 't', 'i', 'n', 'c', 'o', 'a'):  # memperbolehkan huruf untuk fungsi seperti sqrt, sin, tan, dsb.
            return False
    return True