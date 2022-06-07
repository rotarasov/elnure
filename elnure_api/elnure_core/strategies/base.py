import abc


class StrategyError(Exception):
    pass


class BaseChoiceStrategy(abc.ABC):
    def run(self):
        raise NotImplementedError()

    def save_results(self):
        raise NotImplementedError()
