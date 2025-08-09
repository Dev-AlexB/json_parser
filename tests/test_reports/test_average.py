from models import LogRecord
from reports.average import AverageReport


def test_average_report_generate():
    logs = iter(
        [
            LogRecord(url="/a", response_time=1.0),
            LogRecord(url="/a", response_time=2.0),
            LogRecord(url="/b", response_time=3.0),
            LogRecord(url=None, response_time=5.0),
            LogRecord(url="/c", response_time=None),
        ]
    )
    report = AverageReport(logs)
    result = report._generate()
    assert report._headers == ("", "handler", "total", "avg_response_time")
    assert len(result) == 2
    assert result[0] == (0, "/a", 2, 1.5)
    assert result[1] == (1, "/b", 1, 3.0)
