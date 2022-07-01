
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


# Perf
```sh
python3 -m cProfile withcache.py mysql 1 100 3 > withcache.stats
python3 -m cProfile withoutcache.py mysql 1 100 3 > withoutcache.stats
```

# Result

## Format
`ncalls  tottime  percall  cumtime  percall filename:lineno(function)`

- `ncalls` : Shows the number of calls made
- `tottime`: Total time taken by the given function. Note that the time made in calls to sub-functions are excluded.
- `percall`: Total time / No of calls. ( remainder is left out )
- `cumtime`: Unlike tottime, this includes time spent in this and all subfunctions that the higher-level function calls. It is most useful and is accurate for recursive functions.
- The `percall` following cumtime is calculated as the quotient of cumtime divided by primitive calls. The primitive calls include all the calls that were not included through recursion.

## Without cache
```
        1    0.000    0.000    0.139    0.139 storage.py:1(<module>)
      400    0.005    0.000    0.804    0.002 storage.py:1027(<listcomp>)
    15850    0.101    0.000    5.567    0.000 storage.py:1031(_build_frozen_trial_from_trial_model)
    14950    0.002    0.000    0.002    0.000 storage.py:1035(<listcomp>)
    15850    0.057    0.000    0.369    0.000 storage.py:1050(<dictcomp>)
    15850    0.034    0.000    0.323    0.000 storage.py:1056(<dictcomp>)
    15850    0.002    0.000    0.002    0.000 storage.py:1060(<dictcomp>)
    15850    0.002    0.000    0.002    0.000 storage.py:1061(<dictcomp>)
    15850    0.002    0.000    0.002    0.000 storage.py:1064(<dictcomp>)
      400    0.003    0.000    0.609    0.002 storage.py:1091(read_trials_from_remote_storage)
        1    0.000    0.000    0.000    0.000 storage.py:1096(_set_default_engine_kwargs_for_mysql)
        1    0.000    0.000    0.000    0.000 storage.py:1114(_fill_storage_url_template)
        1    0.000    0.000    0.000    0.000 storage.py:1119(remove_session)
      200    0.000    0.000    0.000    0.000 storage.py:1210(get_heartbeat_interval)
        1    0.000    0.000    0.000    0.000 storage.py:1219(_VersionManager)
        1    0.000    0.000    0.071    0.071 storage.py:1220(__init__)
        1    0.000    0.000    0.025    0.025 storage.py:1233(_init_version_info_model)
        1    0.000    0.000    0.045    0.045 storage.py:1246(_init_alembic)
        1    0.000    0.000    0.028    0.028 storage.py:1271(check_table_schema_compatibility)
        1    0.000    0.000    0.004    0.004 storage.py:1303(get_current_version)
        1    0.000    0.000    0.022    0.022 storage.py:1311(get_head_version)
        1    0.000    0.000    0.004    0.004 storage.py:1352(_create_alembic_script)
        1    0.000    0.000    0.004    0.004 storage.py:1358(_create_alembic_config)
        2    0.000    0.000    0.000    0.000 storage.py:1368(escape_alembic_config_value)
        1    0.000    0.000    0.127    0.127 storage.py:185(__init__)
        1    0.000    0.000    0.024    0.024 storage.py:255(create_new_study)
        1    0.000    0.000    0.002    0.002 storage.py:285(_create_unique_study_name)
        1    0.000    0.000    0.012    0.012 storage.py:298(set_study_directions)
        1    0.000    0.000    0.000    0.000 storage.py:303(<listcomp>)
        2    0.000    0.000    0.003    0.001 storage.py:355(get_study_id_from_name)
        1    0.000    0.000    0.002    0.002 storage.py:363(get_study_name_from_id)
      670    0.005    0.000    1.399    0.002 storage.py:371(get_study_directions)
      670    0.001    0.000    0.001    0.000 storage.py:375(<listcomp>)
      300    0.003    0.000    0.680    0.002 storage.py:410(get_trial_system_attrs)
      300    0.000    0.000    0.000    0.000 storage.py:417(<dictcomp>)
      100    0.001    0.000    1.134    0.011 storage.py:545(create_new_trial)
      100    0.002    0.000    1.133    0.011 storage.py:549(_create_new_trial)
      100    0.001    0.000    0.219    0.002 storage.py:608(_get_prepared_new_trial)
     6554    0.011    0.000    5.819    0.001 storage.py:63(_create_scoped_session)
      300    0.001    0.000    3.178    0.011 storage.py:705(set_trial_param)
      300    0.003    0.000    0.878    0.003 storage.py:718(_set_trial_param_without_commit)
      100    0.001    0.000    1.111    0.011 storage.py:798(set_trial_state_values)
      100    0.001    0.000    0.152    0.002 storage.py:825(_set_trial_value_without_commit)
      
     1000    0.010    0.000    6.855    0.007 storage.py:945(get_trial) <--- Here!
      400    0.008    0.000    6.368    0.016 storage.py:953(get_all_trials)  <--- Here!

        1    0.000    0.000    0.000    0.000 storage.py:96(RDBStorage)
      400    0.020    0.000    6.357    0.016 storage.py:964(_get_trials)
    15250    0.002    0.000    0.002    0.000 storage.py:983(<genexpr>)
```

- `storage.get_all_trials`
  - `storage._get_trials` を呼ぶ
- `storage.get_trial`
  - db から直接検索
- `storage.read_trials_from_remote_storage`
  - db から直接検索

## With Cache

```
        1    0.000    0.000    0.136    0.136 _cached_storage.py:1(<module>)
        1    0.000    0.000    0.005    0.005 _cached_storage.py:115(get_study_id_from_name)
        1    0.000    0.000    0.007    0.007 _cached_storage.py:119(get_study_name_from_id)
      670    0.002    0.000    0.002    0.000 _cached_storage.py:134(get_study_directions)
      100    0.001    0.000    1.221    0.012 _cached_storage.py:161(create_new_trial)
      300    0.004    0.000    3.755    0.013 _cached_storage.py:181(set_trial_param)
      100    0.002    0.000    2.137    0.021 _cached_storage.py:237(set_trial_state_values)
        1    0.000    0.000    0.000    0.000 _cached_storage.py:26(_StudyInfo)
        1    0.000    0.000    0.000    0.000 _cached_storage.py:27(__init__)
     1700    0.002    0.000    0.002    0.000 _cached_storage.py:308(_get_cached_trial)

     1300    0.002    0.000    0.004    0.000 _cached_storage.py:315(get_trial) <--- Here!
      400    0.003    0.000    0.020    0.000 _cached_storage.py:324(get_all_trials) <--- Here!

      400    0.006    0.000    0.006    0.000 _cached_storage.py:341(<dictcomp>)
    14850    0.005    0.000    0.007    0.000 _cached_storage.py:344(<lambda>)
      400    0.003    0.000    2.085    0.005 _cached_storage.py:347(read_trials_from_remote_storage)
      100    0.001    0.000    0.001    0.000 _cached_storage.py:361(_add_trials_to_cache)
      400    0.000    0.000    0.001    0.000 _cached_storage.py:371(_check_trial_is_updatable)
        1    0.000    0.000    0.000    0.000 _cached_storage.py:38(_CachedStorage)
      200    0.000    0.000    0.000    0.000 _cached_storage.py:384(get_heartbeat_interval)
        1    0.000    0.000    0.000    0.000 _cached_storage.py:51(__init__)
        1    0.000    0.000    0.026    0.026 _cached_storage.py:67(create_new_study)
        1    0.000    0.000    0.023    0.023 _cached_storage.py:90(set_study_directions)
```

```
        1    0.000    0.000    0.134    0.134 storage.py:1(<module>)
      400    0.000    0.000    0.000    0.000 storage.py:1027(<listcomp>)
      100    0.003    0.000    0.600    0.006 storage.py:1031(_build_frozen_trial_from_trial_model)
      100    0.000    0.000    0.000    0.000 storage.py:1035(<listcomp>)
      100    0.001    0.000    0.009    0.000 storage.py:1050(<dictcomp>)
      100    0.001    0.000    0.005    0.000 storage.py:1056(<dictcomp>)
      100    0.000    0.000    0.000    0.000 storage.py:1060(<dictcomp>)
      100    0.000    0.000    0.000    0.000 storage.py:1061(<dictcomp>)
      100    0.000    0.000    0.000    0.000 storage.py:1064(<dictcomp>)
        1    0.000    0.000    0.000    0.000 storage.py:1096(_set_default_engine_kwargs_for_mysql)
        1    0.000    0.000    0.000    0.000 storage.py:1114(_fill_storage_url_template)
      200    0.000    0.000    0.000    0.000 storage.py:1210(get_heartbeat_interval)
        1    0.000    0.000    0.000    0.000 storage.py:1219(_VersionManager)
        1    0.000    0.000    0.067    0.067 storage.py:1220(__init__)
        1    0.000    0.000    0.023    0.023 storage.py:1233(_init_version_info_model)
        1    0.000    0.000    0.044    0.044 storage.py:1246(_init_alembic)
        1    0.000    0.000    0.028    0.028 storage.py:1271(check_table_schema_compatibility)
        1    0.000    0.000    0.005    0.005 storage.py:1303(get_current_version)
        1    0.000    0.000    0.022    0.022 storage.py:1311(get_head_version)
        1    0.000    0.000    0.004    0.004 storage.py:1352(_create_alembic_script)
        1    0.000    0.000    0.004    0.004 storage.py:1358(_create_alembic_config)
        2    0.000    0.000    0.000    0.000 storage.py:1368(escape_alembic_config_value)
        1    0.000    0.000    0.121    0.121 storage.py:185(__init__)
        1    0.000    0.000    0.026    0.026 storage.py:255(create_new_study)
        1    0.000    0.000    0.002    0.002 storage.py:285(_create_unique_study_name)
        1    0.000    0.000    0.023    0.023 storage.py:298(set_study_directions)
        1    0.000    0.000    0.000    0.000 storage.py:303(<listcomp>)
        2    0.000    0.000    0.012    0.006 storage.py:355(get_study_id_from_name)
        1    0.000    0.000    0.007    0.007 storage.py:363(get_study_name_from_id)
      100    0.002    0.000    1.219    0.012 storage.py:549(_create_new_trial)
      100    0.002    0.000    0.253    0.003 storage.py:608(_get_prepared_new_trial)
     2014    0.005    0.000    4.479    0.002 storage.py:63(_create_scoped_session)
      297    0.002    0.000    3.699    0.012 storage.py:705(set_trial_param)
      297    0.004    0.000    1.378    0.005 storage.py:718(_set_trial_param_without_commit)
        3    0.000    0.000    0.047    0.016 storage.py:752(_check_and_set_param_distribution)
      100    0.002    0.000    1.283    0.013 storage.py:798(set_trial_state_values)
      100    0.002    0.000    0.223    0.002 storage.py:825(_set_trial_value_without_commit)

      100    0.001    0.000    0.852    0.009 storage.py:945(get_trial) <--- Here!

        1    0.000    0.000    0.000    0.000 storage.py:96(RDBStorage)
      400    0.026    0.000    2.083    0.005 storage.py:964(_get_trials)
      400    0.002    0.000    0.002    0.000 storage.py:983(<genexpr>)
```

- `cached_storage.get_all_trials`
  - study_id がメモリになければ `cached_storage.read_trials_from_remote_storage` を呼ぶ
- `cached_storage.get_trial`
  - trial_id がメモリになければ `storage.get_trial` を呼ぶ
- `cached_storage.read_trials_from_remote_storage`
  - `storage._get_trials` を呼ぶ