import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from itertools import chain
from typing import Any, Iterator

from tabulate import tabulate


def validate_date(date: str | None) -> str | None:
    """Валидирует дату при вводе в CLI"""
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
    """Парсит логи, возвращает итератор из всех строк всех лог-файлов.

    Пустые строки игнорирует.
    При ошибке декодирования - игнорирует строку и пишет в std.err.
    При ошибке чтения файла (не существует, ошибка доступа и т.д.) игнорирует
    файл и пишет в std.err, добавляя вместо этого файла пустой итератор
    в общий chain.from_iterable.
    Но если все файлы проигнорированы - выходит из программы и пишет в std.err.
    """
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
    """Строит отчет по логам.

    В конструктор передаются логи в виде итератора из словарей,
    название отчета и даты для фильтрации (может быть равна None,
    тогда фильтрация не производится).

    Вычисления формирующие отчет производятся в момент вызова print_report,
    который выводит отчет на печать. При повторном вызове make_report
    использует ранее сформированный отчет.

    Класс можно расширить добавив новые отчеты, их выбор происходит при
    вызове _make_report внутри класса, где определяется какие будут применены
    фильтры, какие заголовки будут у отчета.

    Функция _group_average реализует отчет 'average' (на данный момент
    единственный). При обработке строк игнорируются строки с ошибками
    при обработке, при этом информация об этих строках выводится в std.err.
    Отчет average считает средне 'response_time' (в выводе 'avg_response_time')
    и кол-во запросов (в выводе 'total') по каждому 'url' (в выводе 'handler'),
    упорядочивает по кол-ву запросов и добавляет столбец с нумерацией с нуля.
    """

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
                    "handler",
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


def main():
    """Точка входа.

    Парсит аргументы из CLI и валидирует их.
    Парсит логи, создает экземпляр ReportBuilder и печатает отчет.
    """
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


if __name__ == "__main__":
    main()
