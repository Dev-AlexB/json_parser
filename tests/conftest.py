import sys

import pytest


@pytest.fixture
def patch_sys_argv(monkeypatch):
    def _patch(args):
        monkeypatch.setattr(sys, "argv", args)

    return _patch
