from unittest.mock import MagicMock

from reports.base import Report


class DummyReport(Report):
    def __init__(self, logs):
        super().__init__(logs, headers=("h1", "h2"))

    def _generate(self):
        return (1, 2), (3, 4)


def test_report(capsys):
    report = DummyReport(iter([]))
    mock_generate = MagicMock(return_value=((3, 4),))
    report._generate = mock_generate
    assert report._rows is None

    report.print()
    out1 = capsys.readouterr().out
    assert {"h1", "h2", "3", "4"}.issubset(out1.split())
    mock_generate.assert_called_once()
    assert report._rows == ((3, 4),)

    report.print()
    out2 = capsys.readouterr().out
    assert out2 == out1
    mock_generate.assert_called_once()
