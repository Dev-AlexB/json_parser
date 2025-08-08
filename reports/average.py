from collections import defaultdict
from typing import Any, Iterator

from models import LogRecord
from reports.base import Report


class AverageReport(Report):
    """Отчет 'average'.

    Переопределяет абстрактный метод _generate,
    который генерирует отчет. Передает заголовки в инициализатор
    родительского класса.
    Класс реализует отчет 'average' (на данный момент
    единственный). При обработке строк игнорируются строки с
    'None' значениями в атрибутах 'response_time' и 'url' LogRecord.
    Отчет average считает средне 'response_time' (в выводе 'avg_response_time')
    и кол-во запросов (в выводе 'total') по каждому 'url' (в выводе 'handler'),
    упорядочивает по кол-ву запросов и добавляет столбец с нумерацией с нуля.
    """

    def __init__(self, logs: Iterator[LogRecord]) -> None:
        headers = ("", "handler", "total", "avg_response_time")
        super().__init__(logs, headers)

    def _generate(self) -> tuple[tuple[Any, ...], ...]:
        groups = defaultdict(lambda: {"count": 0, "sum": 0.0})
        for log in self._logs:
            key = log.url
            value = log.response_time
            if key is None or value is None:
                continue
            groups[key]["count"] += 1
            groups[key]["sum"] += value
        report_data = sorted(
            (
                (k, v["count"], round(v["sum"] / v["count"], 3))
                for k, v in groups.items()
            ),
            key=lambda x: -x[1],
        )
        return tuple((i, *items) for i, items in enumerate(report_data))
