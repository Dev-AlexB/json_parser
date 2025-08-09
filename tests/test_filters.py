from filters import FilterPipeline
from models import LogRecord


def test_filter_pipeline():
    logs = iter(
        [
            LogRecord(url="/a", timestamp="2025-06-11T00:00:00+00:00"),
            LogRecord(url="/a", timestamp="2025-06-22T00:00:00+00:00"),
            LogRecord(url="/a", timestamp=None),
            LogRecord(url="/b", timestamp="2025-06-11T00:00:00+00:00"),
            LogRecord(url="/b", timestamp="2025-06-22T00:00:00+00:00"),
        ]
    )
    pipeline = FilterPipeline()
    pipeline.add_equal("url", "/a")
    pipeline.add_contains("timestamp", "2025-06-11")
    filtered_logs = pipeline.apply(logs)
    assert list(filtered_logs) == [
        LogRecord(url="/a", timestamp="2025-06-11T00:00:00+00:00")
    ]
