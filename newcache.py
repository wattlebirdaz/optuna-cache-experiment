import argparse
from collections import defaultdict
from datetime import datetime
import math
from optuna import storages
from optuna.storages._rdb.storage import RDBStorage
from cached_storage2 import _CachedStorage

import optuna

optuna.logging.set_verbosity(optuna.logging.ERROR)

profile_result = defaultdict(lambda: datetime.now() - datetime.now())


class Profile:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = datetime.now()

    def __exit__(self, exc_type, exc_val, exc_tb):
        profile_result[self.name] += datetime.now() - self.start


def print_profile():
    for key, value in sorted(profile_result.items(), key=lambda i: i[1], reverse=True):
        print(key.ljust(50) + "{}".format(value))


def build_objective_fun(n_param):
    def objective(trial):
        return sum(
            [
                math.sin(trial.suggest_float("param-{}".format(i), 0, math.pi * 2))
                for i in range(n_param)
            ]
        )

    return objective


def define_flags(parser):
    parser.add_argument("backend")
    parser.add_argument("n_study", type=int)
    parser.add_argument("n_trial", type=int)
    parser.add_argument("n_param", type=int)
    return parser


if __name__ == "__main__":
    parser = define_flags(argparse.ArgumentParser())
    args = parser.parse_args()
    print(vars(args))

    if args.backend == "mysql":
        storage = _CachedStorage(RDBStorage("mysql+mysqldb://optuna:password@127.0.0.1:3306/optuna"))
    elif args.backend == "sqlite3":
        storage = _CachedStorage(RDBStorage("sqlite:///db.sqlite3withoutcache"))
    elif args.backend == "postgres":
        storage = _CachedStorage(RDBStorage("postgresql+psycopg2://root:root@localhost:5432/optuna"))
    else:
        raise RuntimeError

    sampler = optuna.samplers.TPESampler()

    def mock_get_storage(mock_storage):
        return storage

    storages.get_storage = mock_get_storage

    for i in range(args.n_study):
        study = optuna.create_study(sampler=sampler, storage=storage)
        study_id = study._study_id
        with Profile("perf:optimize-study:without-cache:" + args.backend):
            study.optimize(
                build_objective_fun(args.n_param),
                n_trials=args.n_trial,
                gc_after_trial=False,
            )

    print_profile()
