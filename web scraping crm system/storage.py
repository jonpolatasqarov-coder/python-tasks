import json
import csv


def save_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


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