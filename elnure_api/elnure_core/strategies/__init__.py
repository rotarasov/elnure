from constance import config
from elnure_core.models import Strategy
from elnure_core.strategies.base import StrategyError
from elnure_core.strategies.default import DefaultChoiceStrategy


HANDLER_MAP = {Strategy.DEFAULT: DefaultChoiceStrategy}


def run_strategy(application_window, strategy=None, *args, **kwargs):
    strategy = strategy or config.STRATEGY

    handler_class = HANDLER_MAP[strategy]
    handler = handler_class(*args, application_window=application_window, **kwargs)
    run_snapshot = handler.run()

    return run_snapshot


def make_run_snapshot_permanent(run_snapshot, *args, **kwargs):
    handle_class = HANDLER_MAP[run_snapshot.strategy]
    handler = handle_class(*args, run_snapshot=run_snapshot, **kwargs)

    return handler.save_results()
