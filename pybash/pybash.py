import subprocess


class PendingCommand:
    def __init__(self, command_line):
        self._command_line = command_line
        self._should_raise = True

    def run(self) -> "CommandResult":
        result = self._run()
        if self._should_raise and result.status != 0:
            raise CommandException(result)
        return result

    def _run(self) -> "CommandResult":
        sp_result = subprocess.run(
            self._command_line,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return CommandResult(sp_result.stdout, sp_result.stderr, sp_result.returncode)

    def should_raise(self, should_it):
        self._should_raise = should_it
        return self

    def stdout(self, *args, file=None):
        return self

    def stderr(self, *args, file=None):
        return self

    def stdin(self, *args, file=None):
        return self

    def or_(self, *args, **kwargs):
        other = _args_to_command(args, kwargs)
        return CompoundOrCommand(self, other)

    def and_(self, *args, **kwargs):
        other = _args_to_command(args, kwargs)
        return CompoundAndCommand(self, other)

    def __repr__(self):
        return f"<PendingCommand: {self._command_line}>"


class CompoundCommand(PendingCommand):
    def __init__(self, left: PendingCommand, right: PendingCommand):
        super().__init__(None)
        self.left = left
        self.right = right

    def __repr__(self):
        return f"<{type(self).__name__}: {self.left!r} {self.right!r}>"


class CompoundOrCommand(CompoundCommand):
    def _run(self):
        left_result = self.left._run()
        if left_result.status == 0:
            return left_result
        return self.right._run()


class CompoundAndCommand(CompoundCommand):
    def _run(self):
        left_result = self.left._run()
        if left_result.status != 0:
            return left_result
        return self.right._run()


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
    def __init__(self, result: "CommandResult"):
        self.result = result


def _args_to_command(args, kwargs) -> PendingCommand:
    if len(args) == 1 and isinstance(args[0], PendingCommand):
        return args[0]
    return cmd(*args, **kwargs)


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
