
import json
import csv
import os
import tempfile


def save_json(data, filename):
    if not data:
        raise ValueError(
            f"Refusing to overwrite {filename} with empty data."
        )

    directory = os.path.dirname(os.path.abspath(filename))
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            delete=False,
            suffix=".tmp"
        ) as file:
            temp_path = file.name
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())

        os.replace(temp_path, filename)
        temp_path = None

    finally:
        if temp_path is not None and os.path.exists(temp_path):
            os.remove(temp_path)


def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def save_csv(data, filename):
    if not data:
        return

    with open(filename, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
