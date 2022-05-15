from abc import ABCMeta


class BaseReader(metaclass=ABCMeta):
    def __init__(self, data_source) -> None:
        self._source = data_source
