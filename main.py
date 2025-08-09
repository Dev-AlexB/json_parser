import argparse

from filters import FilterPipeline
from log_parser import LogParser
from reports.factory import report_factory
from utils import validate_date


def main():
    """Точка входа.

    Парсит аргументы из CLI и валидирует их.
    Парсит логи, применяет фильтры и печатает отчет.
    """
    args_parser = argparse.ArgumentParser()
    # Добавляем аргументы, которые нужно спарсить из CLI.
    # Например, новые фильтры.
    args_parser.add_argument(
        "--file",
        nargs="+",
        help="Название файлов логов или относительные пути к файлам логов",
    )
    #  Тут добавляем в choices новые отчеты и обновляем help
    args_parser.add_argument(
        "--report",
        required=True,
        choices=[
            "average",
        ],
        help="Название отчета, может быть одно из списка: [average,]",
    )
    args_parser.add_argument(
        "--date", type=validate_date, help="Дата в формате ГГГГ-ММ-ДД"
    )
    args = args_parser.parse_args()

    # Получаем итератор из записей в логах
    parsed_logs = LogParser(args.file).parse()

    # Собираем пайплайн из фильтров
    filter_pipeline = FilterPipeline()
    if args.date:
        filter_pipeline.add_contains("timestamp", args.date)
    # Применяем пайплайн из фильтров к итератору логов
    filtered_logs = filter_pipeline.apply(parsed_logs)

    # Фабрика создает объект отчета, выбирая его в зависимости от
    # переданного названия отчета.
    report = report_factory(args.report, filtered_logs)
    # Печатаем выбранный отчет
    report.print()


if __name__ == "__main__":
    main()
