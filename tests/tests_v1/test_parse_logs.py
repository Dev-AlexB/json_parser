import pytest

from main import parse_logs


@pytest.mark.parametrize(
    "log_content, expected_result",
    [
        (
            '{"url": "/home", "response_time": "0.1"}\n',
            [{"url": "/home", "response_time": "0.1"}],
        ),
        (
            '\n{"url": "/home", "response_time": "0.1"}\n\n',
            [{"url": "/home", "response_time": "0.1"}],
        ),
    ],
    ids=["Normal file", "Empty lines"],
)
def test_success(tmp_path, log_content, expected_result):
    log_path = tmp_path / "example.log"
    log_path.write_text(log_content)
    logs = list(parse_logs([str(log_path)]))
    assert logs == expected_result


def test_invalid_line(tmp_path, capsys):
    log_path = tmp_path / "log.json"
    log_path.write_text('{"url": "/home"}\nINVALID\n')
    logs = list(parse_logs([str(log_path)]))
    assert logs == [{"url": "/home"}]
    captured = capsys.readouterr()
    assert "Не удалось спарсить строку" in captured.err


def test_no_file(capsys):
    with pytest.raises(SystemExit):
        list(parse_logs(["nonexistent_file.log"]))
    captured = capsys.readouterr()
    assert "Файл nonexistent_file.log не удалось прочитать" in captured.err
    assert "FileNotFoundError" in captured.err
    assert "Все файлы не существуют либо не читаются" in captured.err


def test_multiple_files(tmp_path):
    f1 = tmp_path / "f1.log"
    f1.write_text('{"url": "/a", "response_time": "1.0"}\n')
    f2 = tmp_path / "f2.log"
    f2.write_text('{"url": "/b", "response_time": "2.0"}\n')
    logs = list(parse_logs([str(f1), str(f2)]))
    assert logs == [
        {"url": "/a", "response_time": "1.0"},
        {"url": "/b", "response_time": "2.0"},
    ]


def test_one_bad_file(tmp_path, capsys):
    good_file = tmp_path / "good.log"
    good_file.write_text('{"url": "/a", "response_time": "0.1"}\n')
    logs = list(parse_logs([str(good_file), "nonexistent.log"]))
    assert logs == [{"url": "/a", "response_time": "0.1"}]
    captured = capsys.readouterr()
    assert "Файл nonexistent.log не удалось прочитать" in captured.err
