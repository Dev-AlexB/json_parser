import pytest

from main import validate_date


def test_validate_date__valid_date():
    assert validate_date("2024-12-27") == "2024-12-27"


def test_validate_date__none_date():
    assert validate_date(None) is None


def test_validate_date__invalid_format(capsys):
    with pytest.raises(SystemExit):
        validate_date("27-12-2024")
    captured = capsys.readouterr()
    text = "Указана некорректная дата 27-12-2024, допустимый формат ГГГГ-ММ-ДД"
    assert text in captured.err
