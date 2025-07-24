import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from itertools import chain
from typing import Any, Iterator

from tabulate import tabulate


def validate_date(date: str | None) -> str | None:
    if date is not None:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print(
                f"Указана некорректная дата {date}, "
                "допустимый формат ГГГГ-ММ-ДД",
                file=sys.stderr,
            )
            sys.exit(1)
    return date


def parse_logs(paths: list[str]) -> Iterator[dict[str, Any]]:
    ok_files_num = len(paths)

    def parse_file(path: str) -> Iterator[dict[str, Any]]:
        nonlocal ok_files_num
        try:
            with open(path, "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except json.JSONDecodeError as e:
                        print(
                            f"Не удалось спарсить строку: '{line}'\n"
                            f"Ошибка: {e!r}",
                            file=sys.stderr,
                        )
        except Exception as e:
            ok_files_num -= 1
            print(
                f"Файл {path} не удалось прочитать, ошибка {e!r}",
                file=sys.stderr,
            )
            if ok_files_num == 0:
                print(
                    "Все файлы не существуют либо не читаются", file=sys.stderr
                )
                sys.exit(1)
            yield from []

    return chain.from_iterable(map(parse_file, paths))


class ReportBuilder:
    def __init__(self, logs, report_name, date):
        self._logs = logs
        self._report_name = report_name
        self._date = date
        self._report = None
        self._report_headers = None

    def _make_report(self):
        match self._report_name:
            case "average":
                self._report = self._filter_date()._group_average(
                    "url", "response_time"
                )
                self._report_headers = [
                    "",
                    "url",
                    "total",
                    "avg_response_time",
                ]
            case _:
                print(
                    f"Недопустимый тип отчета: {self._report_name}",
                    file=sys.stderr,
                )
                sys.exit(1)

    def _filter_date(self):
        if self._date is not None:
            self._logs = filter(
                lambda x: self._date in x.get("@timestamp", ""), self._logs
            )
        return self

    def _group_average(self, group_key, value_key):
        groups = defaultdict(lambda: {"count": 0, "sum": 0.0})
        for log in self._logs:
            try:
                key = log[group_key]
                value = float(log[value_key])
            except Exception as e:
                print(
                    f"Ошибка {e!r} при составлении отчета в строке: '{log}'",
                    file=sys.stderr,
                )
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
        return [(i, *items) for i, items in enumerate(report_data)]

    def print_report(self):
        if self._report is None:
            self._make_report()
        print(tabulate(self._report, headers=self._report_headers))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file",
        nargs="+",
        help="Название файлов логов или относительные пути к файлам логов",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=[
            "average",
        ],
        help="Название отчета, может быть одно из списка: [average,]",
    )
    parser.add_argument(
        "--date", type=validate_date, help="Дата в формате ГГГГ-ММ-ДД"
    )
    args = parser.parse_args()

    parsed_logs = parse_logs(args.file)

    reporter = ReportBuilder(parsed_logs, args.report, args.date)
    reporter.print_report()
