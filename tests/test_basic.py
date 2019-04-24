import pytest

from pybash import run, CommandException


def test_raises_on_fail():
    with pytest.raises(CommandException):
        run("false")


def test_does_not_raise_on_success():
    run("true")
