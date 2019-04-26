# pybash: Write your bash scripts in Python.

  A Python library for bridging the gap between "small enough for Bash" and "why
did ever I think Bash was a good idea?".

  NOTE: despite the name, Bash is not required or supported by this library.
It's just that this library is trying to copy the "feel" of Bash, with some
of the benefits of Python.

  There's no equivalent to subprocess's `shell=True` mode of execution.

## Usage - Quick:
```python
  from bypash import cmd, run, run_

  print(run('git', 'log', '-5', skip=5))   # same as `git log -5 --skip=5`

  run('false') # raise exception.

  if not run_('false'): # Does not raise.
      print('false is falsey')

  # equivalent to `git log --oneline | grep broken':
  c = cmd('git', 'log', '--oneline').stdout('grep', 'broken')
  result = c.run()
  print(result)
  print(result.stderr)
  print(result.status)

  # equivalent to `git log > full-log.txt`
  run('git', 'log', __stdout='full-log.txt')
```

## Usage - Full

The primary entry points to the library are `cmd` and `run` functions.
`run(...)` is shorthand for `cmd(...).run()`. `cmd` has all the good stuff, and
returns a PendingCommand instance - this object supports piping, redirecting,
executing, and all the things we like.
`run()` returns a CommandResult instance, which should to the right thing.

#### `cmd(...)`, `run(...)`, `run_(...)`:

The positional arguments for these functions are all assumed to be a command
(first argument) and its arguments, as strings.

Named arguments that start with `__` (dunder) are options to the
PendingCommand instance - see below for list.

Other named arguments are assumed to be long-form arguments with values:
    `run('git', 'log', skip=5)` is equivalent to `git log --skip=5`.
These are appended after all the positional arguments, but their order is not
guaranteed (because it's a python dict).

`cmd` returns a PendingCommand instance.

`run(...)` is short for `cmd(...).run()`, and returns CommandResult.

`run_(...)` is short for `run(..., __raise=False)`.


### PendingCommand class:

Instances of this class are mutable.

Methods that chain or pipe commands return a new instance.
Methods that configure the command return `self`.

####  `.run()`
Executes the command, returns a CommandResult.

####  `.should_raise(bool)`;  cmd argument `__raise`:
By default, `run()` will raise a CommandException if the exit status is
  non-0. Set this to False to change not raising.
  Can also be provided in the `cmd()` constructor as `__raise=False`.


#### `.stdout()`;  cmd argument `__stdout`
#### `.stderr()`;   cmd argument `__stderr`
#### `.stdin()`;   cmd argument `__stdin`:

If these methods receive only one argument, and that argument is a
file-object, the relevant stream is redirected to/from this file-object. If
it's a PendingCommand instance, the two commands are piped together.
If they receive a single named parameter `file`, this may be either a string
(which is interpreted as a filename) or a file-object.
Otherwise, the arguments are assumed to be the inputs for `cmd`, and the two
commands are piped together.

### CommandResult class:
Instances of this class are immutable, and they keep the entire outputs from
the execution in memory. Try to avoid keeping them for programs with lots of
output.

If considered as a string, this is just the stdout of the command.

If considered as a bool, it's truethy if the exit status of the command was 0,
falsey otherwise. Note that by default `run` just throws on non-0 exits!

  Other members:

#### `.stdout`, `.stderr`:
strings, the standard and error outputs of the program.
#### `.status`:
the exit status (int).


### CommandException class:
  Raised when a command exits with a non-0 status.

  Members:
####  `.result`:
  the CommandResult instance for the command.

##    Not Defined Yet
- Process Substitution (`diff <(run some code) <(run some other code)`)
- Background processes (`ls &`)
