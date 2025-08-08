import pytest

from utils import float_or_none, int_or_none, validate_date


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


@pytest.mark.parametrize(
    "value, expectation",
    [("85", 85), ("85,7", None), ("not_num", None)],
    ids=["integer", "float", "not number"],
)
def test_int_or_none(value, expectation):
    assert int_or_none(value) == expectation


@pytest.mark.parametrize(
    "value, expectation",
    [("85", 85.0), ("85.7", 85.7), ("not_num", None)],
    ids=["integer", "float", "not number"],
)
def test_float_or_none(value, expectation):
    assert float_or_none(value) == expectation
