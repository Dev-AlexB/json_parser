import pytest

from models import LogRecord


@pytest.mark.parametrize(
    "data, expectation",
    [
        (
            {
                "@timestamp": "2025-06-22T00:00:00+00:00",
                "status": 200,
                "url": "/api",
                "request_method": "GET",
                "response_time": 0.024,
                "http_user_agent": "Chrome/1.0",
            },
            LogRecord(
                timestamp="2025-06-22T00:00:00+00:00",
                status=200,
                url="/api",
                request_method="GET",
                response_time=0.024,
                http_user_agent="Chrome/1.0",
            ),
        ),
        (
            {
                "@timestamp": "2025-06-22T00:00:00+00:00",
                "url": "/api",
                "response_time": 0.024,
            },
            LogRecord(
                timestamp="2025-06-22T00:00:00+00:00",
                status=None,
                url="/api",
                request_method=None,
                response_time=0.024,
                http_user_agent=None,
            ),
        ),
        (
            {
                "@timestamp": "2025-06-22T00:00:00+00:00",
                "status": "OK",
                "url": "/api",
                "request_method": "GET",
                "response_time": "too_much",
                "http_user_agent": "Chrome/1.0",
            },
            LogRecord(
                timestamp="2025-06-22T00:00:00+00:00",
                status=None,
                url="/api",
                request_method="GET",
                response_time=None,
                http_user_agent="Chrome/1.0",
            ),
        ),
    ],
    ids=[
        "Normal data",
        "Missed fields",
        "Wrong type in status and response_time",
    ],
)
def test_from_dict(data, expectation):
    assert LogRecord.from_dict(data) == expectation
