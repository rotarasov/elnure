from abc import ABCMeta


class BaseWriter(metaclass=ABCMeta):
    def __init__(self, to):
        self._to = to
