from dataclasses import dataclass

from utils import float_or_none, int_or_none


@dataclass
class LogRecord:
    """DTO для хранения информации об отдельной строке лога.

    Метод from_dict создает экземпляр из словаря,
    игнорирую лишние поля. Если значение атрибута
    должно быть int или float, то, в случае ошибки
    преобразования типа, заменяет значение на None.
    """

    timestamp: str | None = None
    status: int | None = None
    url: str | None = None
    request_method: str | None = None
    response_time: float | None = None
    http_user_agent: str | None = None

    @staticmethod
    def from_dict(data: dict) -> "LogRecord":
        return LogRecord(
            timestamp=data.get("@timestamp"),
            status=int_or_none(data.get("status")),
            url=data.get("url"),
            request_method=data.get("request_method"),
            response_time=float_or_none(data.get("response_time")),
            http_user_agent=data.get("http_user_agent"),
        )
