import pytest

from main import main


def test_valid_args(tmp_path, patch_sys_argv, capsys):
    log_path = tmp_path / "1.log"
    log_text = (
        '{"@timestamp": "2025-06-22T14:10:11+00:00", '
        '"url": "/a", "response_time": "0.1"}\n'
    )
    log_path.write_text(log_text)
    patch_sys_argv(
        [
            "main.py",
            "--file",
            str(log_path),
            "--report",
            "average",
            "--date",
            "2025-06-22",
        ]
    )
    main()
    output = capsys.readouterr().out
    assert "/a" in output
    assert "0.1" in output


def test_missing_required_arg(patch_sys_argv, capsys):
    patch_sys_argv(["main.py", "--file", "1.log", "2.log"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "the following arguments are required: --report" in captured.err


def test_invalid_date(patch_sys_argv, capsys):
    patch_sys_argv(
        [
            "main.py",
            "--file",
            "1.log",
            "--report",
            "average",
            "--date",
            "11-03-2025",
        ]
    )
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert (
        "Указана некорректная дата 11-03-2025," " допустимый формат ГГГГ-ММ-ДД"
    ) in captured.err


def test_invalid_report(patch_sys_argv, capsys):
    patch_sys_argv(["main.py", "--file", "1.log", "--report", "nothing"])
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "argument --report: invalid choice: 'nothing'" in captured.err
