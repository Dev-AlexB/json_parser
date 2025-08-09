import pytest

from reports.average import AverageReport
from reports.factory import report_factory


def test_report_factory_success():
    assert isinstance(report_factory("average", iter([])), AverageReport)


def test_report_factory_fail(capsys):
    with pytest.raises(SystemExit):
        report_factory("unknown", iter([]))
    err = capsys.readouterr().err
    assert "Неизвестный тип отчета: unknown" in err
