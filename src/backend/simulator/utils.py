import csv
from pathlib import Path


def write_headers(file_path: Path, is_eve: bool) -> None:
    base_headers = [
        "L",
        "N",
        "K",
        "QBER",
        "ERRORS",
        "QBER_TYPE",
        "REP",
        "TAU_MISSES",
        "TIME",
        "REPETITIONS",
    ]
    eve_headers = ["EVE_SUCCESS", "EVE_REQUIRED"] if is_eve else []
    write_row(file_path, base_headers + eve_headers)


def write_row(file_path: Path, row_values: list[str]) -> None:
    if not str(file_path).endswith("csv"):
        file_path = Path(str(file_path) + ".csv")
    with open(file_path, "a+", newline="") as file:
        w = csv.writer(file, delimiter=";")
        w.writerow(row_values)
