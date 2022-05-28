import abc

from elnure_core.models import ApplicationWindow, StrategyResult


class StrategyError(Exception):
    pass


class BaseChoiceStrategy(abc.ABC):
    def handle(self, application_window: ApplicationWindow):
        raise NotImplementedError()

    def save_strategy_result(self, result: StrategyResult):
        raise NotImplementedError()
