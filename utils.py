def format_number_gr(value, symbol=""):
    """Μορφοποίηση αριθμού σε ελληνικό στυλ: κόμμα για δεκαδικά, τελεία για χιλιάδες"""
    try:
        formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{formatted} {symbol}".strip()
    except Exception:
        return str(value)

def parse_gr_number(x):
    try:
        if isinstance(x, (float, int)):
            return x
        return float(x.replace(".", "").replace(",", "."))
    except:
        return None

def format_percentage_gr(value, decimals=2):
    if value is None:
        return "-"
    sign = "-" if value < 0 else ""
    abs_val = abs(value)
    formatted = f"{abs_val:,.{decimals}f}".replace(",", "#").replace(".", ",").replace("#", ".")
    return f"{sign}{formatted}%"
