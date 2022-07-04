import copy
import threading
from typing import Any
from typing import Callable
from typing import Container
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Set
from typing import Tuple
from typing import Union

import optuna
from optuna import distributions
from optuna.storages import BaseStorage
from optuna.storages._heartbeat import BaseHeartbeat
from optuna.storages._rdb.storage import RDBStorage
from optuna.storages._redis import RedisStorage
from optuna.study._study_direction import StudyDirection
from optuna.study._study_summary import StudySummary
from optuna.trial import FrozenTrial
from optuna.trial import TrialState


def log(func):
    return func
# def log(func):
#     def wrapper(*args, **kwargs):
#         result = func(*args, **kwargs)
#         print(func.__name__)
#         return result
#     return wrapper

class _CachedStorage(BaseStorage, BaseHeartbeat):
    """A wrapper class of storage backends.

    This class is used in :func:`~optuna.get_storage` function and automatically
    wraps :class:`~optuna.storages.RDBStorage` class or
    :class:`~optuna.storages.RedisStorage` class.

    Args:
        backend:
            :class:`~optuna.storages.RDBStorage` class or :class:`~optuna.storages.RedisStorage`
            class instance to wrap.
    """

    @log
    def __init__(self, backend: Union[RDBStorage, RedisStorage]) -> None:
        self._backend = backend
        self.trials : Dict[int: FrozenTrial] = dict()

    @log
    def create_new_study(self, study_name: Optional[str] = None) -> int:
        return self._backend.create_new_study(study_name)

    @log
    def delete_study(self, study_id: int) -> None:
        self._backend.delete_study(study_id)

    @log
    def set_study_directions(self, study_id: int, directions: Sequence[StudyDirection]) -> None:
        self._backend.set_study_directions(study_id, directions)

    @log
    def set_study_user_attr(self, study_id: int, key: str, value: Any) -> None:

        self._backend.set_study_user_attr(study_id, key, value)

    @log
    def set_study_system_attr(self, study_id: int, key: str, value: Any) -> None:

        self._backend.set_study_system_attr(study_id, key, value)

    @log
    def get_study_id_from_name(self, study_name: str) -> int:

        return self._backend.get_study_id_from_name(study_name)

    @log
    def get_study_name_from_id(self, study_id: int) -> str:
        return self._backend.get_study_name_from_id(study_id)

    @log
    def get_study_directions(self, study_id: int) -> List[StudyDirection]:

        return self._backend.get_study_directions(study_id)

    @log
    def get_study_user_attrs(self, study_id: int) -> Dict[str, Any]:

        return self._backend.get_study_user_attrs(study_id)

    @log
    def get_study_system_attrs(self, study_id: int) -> Dict[str, Any]:

        return self._backend.get_study_system_attrs(study_id)

    @log
    def get_all_study_summaries(self, include_best_trial: bool) -> List[StudySummary]:

        return self._backend.get_all_study_summaries(include_best_trial=include_best_trial)

    @log
    def create_new_trial(self, study_id: int, template_trial: Optional[FrozenTrial] = None) -> int:
        frozen_trial = self._backend._create_new_trial(study_id, template_trial)
        trial_id = frozen_trial._trial_id
        self.trials[trial_id] = frozen_trial
        return trial_id

    @log
    def set_trial_param(
        self,
        trial_id: int,
        param_name: str,
        param_value_internal: float,
        distribution: distributions.BaseDistribution,
    ) -> None:
        self._backend.set_trial_param(trial_id, param_name, param_value_internal, distribution)
        self.trials[trial_id].params[param_name] = distribution.to_external_repr(param_value_internal)
        self.trials[trial_id].distributions[param_name] = distribution

    @log
    def get_trial_id_from_study_id_trial_number(self, study_id: int, trial_number: int) -> int:

        return self._backend.get_trial_id_from_study_id_trial_number(study_id, trial_number)

    @log
    def get_best_trial(self, study_id: int) -> FrozenTrial:

        return self._backend.get_best_trial(study_id)

    @log
    def set_trial_state_values(
        self, trial_id: int, state: TrialState, values: Optional[Sequence[float]] = None
    ) -> bool:

        ret = self._backend.set_trial_state_values(trial_id, state=state, values=values)
        self.trials[trial_id].state = state
        self.trials[trial_id].values = values
        return ret

    @log
    def set_trial_intermediate_value(
        self, trial_id: int, step: int, intermediate_value: float
    ) -> None:
        self._backend.set_trial_intermediate_value(trial_id, step, intermediate_value)
        self.trials[trial_id].intermediate_values[step] = intermediate_value

    @log
    def set_trial_user_attr(self, trial_id: int, key: str, value: Any) -> None:

        #self._backend.set_trial_user_attr(trial_id, key=key, value=value)
        self.trials[trial_id].user_attrs[key] = value

    @log
    def set_trial_system_attr(self, trial_id: int, key: str, value: Any) -> None:

        #self._backend.set_trial_system_attr(trial_id, key=key, value=value)
        self.trials[trial_id].system_attrs[key] = value

    @log
    def get_trial(self, trial_id: int) -> FrozenTrial:
        return self.trials[trial_id]
        #return self._backend.get_trial(trial_id)

    @log
    def get_all_trials(
        self,
        study_id: int,
        deepcopy: bool = True,
        states: Optional[Container[TrialState]] = None,
    ) -> List[FrozenTrial]:
        return self._backend.get_all_trials(study_id, deepcopy, states)

    @log
    def read_trials_from_remote_storage(self, study_id: int) -> None:
        return self._backend.read_trials_from_remote_storage(study_id)

    @staticmethod
    @log
    def _check_trial_is_updatable(trial: FrozenTrial) -> None:
        if trial.state.is_finished():
            raise RuntimeError(
                "Trial#{} has already finished and can not be updated.".format(trial.number)
            )

    @log
    def record_heartbeat(self, trial_id: int) -> None:
        self._backend.record_heartbeat(trial_id)

    @log
    def _get_stale_trial_ids(self, study_id: int) -> List[int]:
        return self._backend._get_stale_trial_ids(study_id)

    @log
    def get_heartbeat_interval(self) -> Optional[int]:
        return self._backend.get_heartbeat_interval()

    @log
    def get_failed_trial_callback(self) -> Optional[Callable[["optuna.Study", FrozenTrial], None]]:
        return self._backend.get_failed_trial_callback()
