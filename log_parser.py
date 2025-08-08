import json
import sys
from typing import Iterator

from models import LogRecord


class LogParser:
    """Парсит логи.

    При инициализации принимает список названий/путей к файлам логов.
    Метод parse возвращает итератор из всех строк всех лог-файлов.
    Пустые строки игнорирует.
    При ошибке декодирования - игнорирует строку и пишет в std.err.
    При ошибке чтения файла (не существует, ошибка доступа и т.д.) игнорирует
    файл и пишет в std.err.
    Если все файлы проигнорированы - выходит из программы и пишет в std.err.
    """

    def __init__(self, paths: list[str]) -> None:
        self.paths = paths

    def parse(self) -> Iterator[LogRecord]:
        ok_files: int = 0

        for path in self.paths:
            try:
                yield from self._parse_file(path)
                ok_files += 1
            except Exception as e:
                print(
                    f"Файл {path} не удалось прочитать, ошибка {e!r}",
                    file=sys.stderr,
                )
        if ok_files == 0:
            print("Все файлы не существуют либо не читаются", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def _parse_file(path: str) -> Iterator[LogRecord]:
        with open(path, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    raw = json.loads(line)
                    yield LogRecord.from_dict(raw)
                except json.JSONDecodeError as e:
                    print(
                        f"Не удалось спарсить строку: '{line}'\n"
                        f"Ошибка: {e!r}",
                        file=sys.stderr,
                    )
