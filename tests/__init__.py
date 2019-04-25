from os import path


def exec_path(program):
    return path.join(path.dirname(__file__), "executables", program)
