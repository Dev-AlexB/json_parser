import pytest

from main import ReportBuilder


def test_success():
    logs = iter(
        [
            {"url": "/a", "response_time": "1.0"},
            {"url": "/a", "response_time": "2.0"},
            {"url": "/b", "response_time": "3.0"},
        ]
    )
    rb = ReportBuilder(logs, "average", None)
    rb._make_report()
    assert rb._report == [
        (0, "/a", 2, 1.5),
        (1, "/b", 1, 3.0),
    ]


def test_invalid_value(capsys):
    logs = iter(
        [
            {"url": "/a", "response_time": "1.0"},
            {"url": "/b", "response_time": "bad"},
        ]
    )
    rb = ReportBuilder(logs, "average", None)
    rb._make_report()
    captured = capsys.readouterr()
    assert "Ошибка ValueError" in captured.err
    assert rb._report == [
        (0, "/a", 1, 1.0),
    ]


def test_invalid_report_name(capsys):
    logs = iter([])
    rb = ReportBuilder(logs, "invalid", None)
    with pytest.raises(SystemExit):
        rb._make_report()
    captured = capsys.readouterr()
    assert "Недопустимый тип отчета: invalid" in captured.err


def test_filter_by_date():
    logs = iter(
        [
            {
                "@timestamp": "2025-06-01T00:00:00+00:00",
                "url": "/a",
                "response_time": "1.0",
            },
            {
                "@timestamp": "2025-06-02T00:00:00+00:00",
                "url": "/b",
                "response_time": "2.0",
            },
        ]
    )
    rb = ReportBuilder(logs, "average", "2025-06-01")
    rb._make_report()
    assert rb._report == [(0, "/a", 1, 1.0)]


def test_print_report(capsys):
    logs = iter(
        [
            {"url": "/a", "response_time": "0.1"},
        ]
    )
    rb = ReportBuilder(logs, "average", None)
    rb.print_report()
    assert rb._report == [(0, "/a", 1, 0.1)]
    output = capsys.readouterr().out
    assert "/a" in output
    assert "0.1" in output
