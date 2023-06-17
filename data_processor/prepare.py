import csv


from neural_crypto.data_processor.common import (
    RANDOM_QBER_TEST_DATA_PATH,
    RANDOM_QBER_DATA_PATH,
    BURSTY_QBER_TEST_DATA_PATH,
    BURSTY_QBER_DATA_PATH,
    PREPARED_DATA_HEADER,
    QBERType,
    RAW_TESTING_DATASET_PATH,
    RAW_TRAINING_DATASET_PATH,
)

def write_prepared_data(path: str, is_test_data: bool=False) -> None:
    with open(path, 'r') as file:
        reader = csv.reader(file,  delimiter =';')
        prepared_data_random_qber_filename = RANDOM_QBER_TEST_DATA_PATH if is_test_data else RANDOM_QBER_DATA_PATH
        prepared_data_bursty_qber_filename = BURSTY_QBER_TEST_DATA_PATH if is_test_data else BURSTY_QBER_DATA_PATH

        with open(prepared_data_random_qber_filename, 'w+', newline='') as random_qber_file,\
                open(prepared_data_bursty_qber_filename, 'w+',  newline='') as bursty_qber_file:
                    random_qber_writer = csv.writer(random_qber_file)
                    bursty_qber_writer = csv.writer(bursty_qber_file)
                    random_qber_writer.writerow(PREPARED_DATA_HEADER)
                    bursty_qber_writer.writerow(PREPARED_DATA_HEADER)
                    next(reader, None) # skip header
                    for row in reader:
                        required_data = [*row[0:4], row[-1]]
                        if row[5] == QBERType.RANDOM:
                            random_qber_writer.writerow(required_data)
                        elif row[5] == QBERType.BURSTY:
                            bursty_qber_writer.writerow(required_data)



if __name__ == '__main__':
    write_prepared_data(RAW_TRAINING_DATASET_PATH, is_test_data=False)
    write_prepared_data(RAW_TESTING_DATASET_PATH, is_test_data=True)
