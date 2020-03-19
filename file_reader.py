from classes import Clause


def read(filepath):
    return [Clause([("p", True), ("q", True)]), Clause([("p", False), ("q", True)])]