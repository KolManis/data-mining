"""Задача 1. Поиск выбросов в данных о посещаемости по правилу IQR."""
import sys


def median(values):
    n = len(values)
    mid = n // 2
    if n % 2 == 1:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2


def quartiles(values):
    """Квартили по алгоритму из условия: Q1 и Q3 — медианы нижней и верхней половин.

    При нечётном N центральный элемент не входит ни в одну из половин.
    """
    data = sorted(values)
    n = len(data)
    lower = data[:n // 2]
    upper = data[(n + 1) // 2:]
    return median(lower), median(data), median(upper)


def count_outliers(values):
    q1, _, q3 = quartiles(values)
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return sum(1 for x in values if x < low or x > high)


def main():
    tokens = sys.stdin.read().split()
    n = int(tokens[0])
    values = [int(x) for x in tokens[1:n + 1]]
    print(count_outliers(values))


if __name__ == "__main__":
    main()
