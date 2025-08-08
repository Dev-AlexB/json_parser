import sys
from datetime import datetime


def validate_date(date: str | None) -> str | None:
    """Валидирует дату при вводе в CLI"""
    if date is not None:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(
                f"Указана некорректная дата {date}, "
                "допустимый формат ГГГГ-ММ-ДД",
                file=sys.stderr,
            )
            sys.exit(1)
    return date


def int_or_none(value: str) -> int | None:
    """Преобразует str к int, в случае ошибки возвращает None"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def float_or_none(value: str) -> float | None:
    """Преобразует str к float, в случае ошибки возвращает None"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
