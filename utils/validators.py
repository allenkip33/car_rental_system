from datetime import date


def validate_date(date_text):
    try:
        date.fromisoformat(date_text)
        return True
    except (ValueError, TypeError):
        return False


def validate_price(price):
    try:
        return float(price) > 0
    except (ValueError, TypeError):
        return False


def validate_required(value):
    return bool(value and value.strip())


def validate_year( year):
    try:
        year = int(year )
        return 1900 <= year<= 2100
    except (ValueError, TypeError):
        return False