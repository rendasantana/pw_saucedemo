# utils/data_reader.py
import csv
from pathlib import Path

def read_csv(file_name):
    data = []
    path = Path("data") / file_name
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data
