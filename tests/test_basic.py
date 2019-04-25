import pytest

from . import exec_path as p
from pybash import run, CommandException


def test_raises_on_fail():
    with pytest.raises(CommandException):
        run("false")


def test_does_not_raise_when_asked():
    result = run("false", __raise=False)
    assert result.status != 0


def test_does_not_raise_on_success():
    run("true")


def test_no_trim_output():
    text = run(p("print-text"))  # can I do this by mocking run()?
    text = str(text)
    assert text[0] == text[-1] == text[-2] == "\n"
