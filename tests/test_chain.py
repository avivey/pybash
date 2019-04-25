import pytest
from unittest.mock import patch, MagicMock, sentinel

from pybash.pybash import PendingCommand, CommandResult, CompoundCommand, cmd


def mock_cmd(succeed=True):
    command = MagicMock(spec=PendingCommand)
    command._run.return_value = CommandResult("", "", 0 if succeed else 1)
    return command


def test_chain_with_or():
    command_1 = cmd("false")
    command_2 = mock_cmd()

    compound = command_1.or_(command_2)
    compound.run()

    command_2._run.assert_called_once()

    command_1 = cmd("true")
    command_2.reset_mock()

    compound = command_1.or_(command_2)
    compound.run()

    command_2._run.assert_not_called()


def test_chain_with_and():
    command_1 = cmd("false")
    command_2 = mock_cmd()

    compound = command_1.and_(command_2)
    compound.should_raise(False)
    compound.run()

    command_2._run.assert_not_called()

    command_1 = cmd("true")

    compound = command_1.and_(command_2)
    compound.run()

    command_2._run.assert_called_once()


@pytest.mark.xfail
def test_chains_evaluate_left_to_right():
    assert 0


def test_chain_with_strings():
    compound = cmd("true").and_(sentinel.some_value)
    assert isinstance(compound, CompoundCommand)
    assert compound.right._command_line == [sentinel.some_value]
