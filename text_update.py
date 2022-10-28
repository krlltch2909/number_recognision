import re


def compare_number(text: str) -> bool:
    if re.match(r'\D{1}\d{3}\D{2}\d{2,3}', text) and (len(text) == 9 or len(text) == 8):
        return True
    else:
        return False
