
# Build
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade setuptools pip
pip3 install -r requirements.txt

## Editable install optuna
git clone git@github.com:optuna/optuna.git
cd optuna
pip3 install -e .
cd ../

./mysql.sh
./postgres.sh
```

# Run

```sh
$ python3 cache_experiment.py mysql 1 100 3
{'backend': 'mysql', 'n_study': 1, 'n_trial': 100, 'n_param': 3}
perf:optimize-study:without-cache:mysql           0:00:26.041815
perf:optimize-study-with-cache:mysql              0:00:12.413146
$
```

```sh
$ python3 cache_experiment.py postgres 1 100 3
{'backend': 'postgres', 'n_study': 1, 'n_trial': 100, 'n_param': 3}
perf:optimize-study:without-cache:postgres        0:00:10.264925
perf:optimize-study-with-cache:postgres           0:00:03.954303
```