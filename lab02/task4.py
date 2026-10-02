"""Задача 4. Авторы писем в mbox.txt и самый активный из них.

Если рядом лежит mbox.txt, он читается локально, иначе скачивается.
"""
import os
from collections import Counter

URL = "https://www.py4e.com/code3/mbox.txt"
LOCAL = "mbox.txt"


def load_lines():
    if os.path.exists(LOCAL):
        with open(LOCAL, encoding="utf-8") as f:
            return f.read().split("\n")
    import requests
    return requests.get(URL).text.split("\n")


def main():
    all_lines = load_lines()
    authors = [line.split()[1] for line in all_lines
               if line.startswith("From ") and len(line.split()) > 1]
    counts = Counter(authors)

    print(f"Всего писем: {len(authors)}, уникальных авторов: {len(counts)}")
    for address, count in counts.most_common():
        print(f"{address} - {count}")

    address, count = counts.most_common(1)[0]
    print(f"\nБольше всех писем пишет {address}: {count}")


if __name__ == "__main__":
    main()
