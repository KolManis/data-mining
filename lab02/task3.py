"""Задача 3. Анализ записей о заказах пиццерии.

Запуск: python task3.py [файл]   (по умолчанию orders.txt)
"""
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal

SEP = r"(?:\s*[,;]\s*|\s+)"
LINE_RE = re.compile(
    r"^(?P<day>\d{1,2})[./](?P<month>\d{1,2})[./](?P<year>\d{4})"
    + SEP
    + r"(?P<name>.+?)"  # ленивый захват: стоимостью считается последнее число строки
    + SEP
    + r"(?P<price>\d+(?:[.,]\d{1,2})?)$"
)
QUOTES = "\"'«»“”"


def parse_line(line):
    match = LINE_RE.match(line.strip())
    if not match:
        return None
    try:
        date = datetime(int(match["year"]), int(match["month"]), int(match["day"])).date()
    except ValueError:
        return None
    name = match["name"].strip().strip(QUOTES).strip()
    if not name:
        return None
    price = Decimal(match["price"].replace(",", "."))
    return date, name, price


def read_orders(path):
    with open(path, encoding="utf-8") as f:
        return [order for order in map(parse_line, f) if order]


def fmt_date(date):
    return date.strftime("%d.%m.%Y")


def report(orders):
    print("а)")
    counts = Counter(name for _, name, _ in orders)
    for name, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"{name} - {count}")

    print("б)")
    by_date = defaultdict(Decimal)
    for date, _, price in orders:
        by_date[date] += price
    for date in sorted(by_date):
        print(fmt_date(date), f"{by_date[date]:.2f}")

    print("в)")
    date, name, price = max(orders, key=lambda x: x[2])
    print(fmt_date(date), name, f"{price:.2f}")

    print("г)")
    average = sum(price for _, _, price in orders) / len(orders)
    print(f"{average:.2f}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "orders.txt"
    orders = read_orders(path)
    if not orders:
        print("Нет корректных записей")
        return
    report(orders)


if __name__ == "__main__":
    main()
