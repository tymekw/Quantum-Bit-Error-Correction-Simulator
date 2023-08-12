from dataclasses import dataclass


@dataclass
class QBERType:
    RANDOM = 'random'
    BURSTY = 'bursty'


@dataclass(frozen=True)
class ColumnsDataStats:
    L = 0
    N_K = 1
    QBER = 2
    MEAN_TAU_MISSED = 3
    REPS_MAX = 4
    REPS_MIN = 5
    REPS_MEAN = 6
    REPS_MEDIAN = 7
    REPS_STD_DEV = 8
    REPS_VAR = 9


PATH_TO_RAW_DATA_RESULTS = 'results/data/raw/'
PATH_TO_PREPARED_RESULTS = 'results/data/prepared/'
PATH_TO_PLOTS = 'results/plots'
RAW_DATASET_PATH = PATH_TO_RAW_DATA_RESULTS + 'raw_data.csv'

PREPARED_DATA_FILENAME = 'prepared_data'
STATS_DATA_FILENAME = 'stats'
RANDOM_QBER_DATA_PATH = PATH_TO_PREPARED_RESULTS + PREPARED_DATA_FILENAME + '_' + QBERType.RANDOM + '.csv'
BURSTY_QBER_DATA_PATH = PATH_TO_PREPARED_RESULTS + PREPARED_DATA_FILENAME + '_' + QBERType.BURSTY + '.csv'

RANDOM_QBER_STATS_DATA_PATH = PATH_TO_PREPARED_RESULTS + STATS_DATA_FILENAME + '_' + QBERType.RANDOM + '.csv'
BURSTY_QBER_STATS_DATA_PATH = PATH_TO_PREPARED_RESULTS + STATS_DATA_FILENAME + '_' + QBERType.BURSTY + '.csv'

PREPARED_DATA_HEADER = ['L', 'N', 'K', 'QBER', 'TAU_MISSES', 'REPETITIONS']
STATS_DATA_HEADER = ['L', 'N', 'K', 'QBER', 'MEAN_TAU_MISSES', 'MAX_REPS', 'MIN_REPS', 'MEAN_REPS', 'MEDIAN_REPS',
                     'STD_DEV', 'VAR']
