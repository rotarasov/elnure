import abc

from elnure_core.models import ApplicationWindow, StrategyResult


class BaseChoiceStrategy(abc.ABCMeta):
    def handle(self, application_window: ApplicationWindow):
        raise NotImplementedError()

    def save_strategy_result(self, result: StrategyResult):
        raise NotImplementedError()
