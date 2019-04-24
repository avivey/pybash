import subprocess


class PendingCommand:
    def __init__(self, command_line):
        self._command_line = command_line
        self._should_raise = True

    def run(self) -> "CommandResult":
        sp_result = subprocess.run(
            self._command_line,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        result = CommandResult(sp_result.stdout, sp_result.stderr, sp_result.returncode)
        if self._should_raise and result.status != 0:
            raise CommandException(result)
        return result

    def should_raise(self, should_it):
        self._should_raise = should_it
        return self

    def stdout(self, *args, file=None):
        return self

    def stderr(self, *args, file=None):
        return self

    def stdin(self, *args, file=None):
        return self


class CompoundCommand(PendingCommand):
    def __init__(self, result: "CommandResult"):
        self.result = result


class CommandResult:
    stdout: str
    strerr: str
    status: int

    def __init__(self, stdout, stderr, status):
        self.stdout = stdout
        self.stderr = stderr
        self.status = status

    def __bool__(self) -> bool:
        return self.status == 0

    def __str__(self) -> str:
        return self.stdout


class CommandException(Exception):
    pass


def cmd(*args, **kwargs) -> PendingCommand:
    command_line = list(args)

    options = dict()

    for key, value in kwargs.items():
        if key.startswith("__"):
            options[key] = value
        else:
            command_line.append(f"--{key}={value}")

    command = PendingCommand(command_line)

    for key, value in options.items():
        if key == "__raise":
            command.should_raise(value)
        elif key == "__stdout":
            command.stdout(file=value)
        elif key == "__stderr":
            command.stderr(file=value)
        elif key == "__stdin":
            command.stdin(file=value)
        else:
            raise ValueError(f"Unexpected option key: {key}")

    return command


def run(*args, **kwargs) -> CommandResult:
    return cmd(*args, **kwargs).run()
