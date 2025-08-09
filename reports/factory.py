import sys
from typing import Iterator

from models import LogRecord
from reports.average import AverageReport
from reports.base import Report


def report_factory(report_name: str, logs: Iterator[LogRecord]) -> Report:
    """Фабрика отчетов.

    Возвращает экземпляр отчета в зависимости от имени отчета,
    которое передается в функцию вместе с итератором из логов.
    Для добавления новых отчетов требуется расширить словарь reports.
    """
    reports: dict[str, type[Report]] = {
        "average": AverageReport,
    }
    report_class = reports.get(report_name)
    if report_class is None:
        print(
            f"Неизвестный тип отчета: {report_name}",
            file=sys.stderr,
        )
        sys.exit(1)
    return report_class(logs)
