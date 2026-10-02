"""Задача 2. Расчёт переводов между участниками похода.

Все суммы считаются в копейках (целые числа), чтобы избежать ошибок округления.

Минимальное число переводов: если разбить участников с ненулевым балансом
на максимальное число групп, внутри каждой из которых долги взаимно гасятся,
то ответ равен (число участников - число групп), так как группе из k человек
достаточно k - 1 перевода. Точное разбиение ищется динамикой по подмножествам;
при очень большом числе участников используется эвристика.
"""
import sys

EXACT_LIMIT = 18


def fmt(cents):
    return f"{cents // 100}.{cents % 100:02d}"


def read_input(stream):
    lines = [line.strip() for line in stream if line.strip()]
    names = lines[0].split()
    n = int(lines[1])
    paid = {name: 0 for name in names}
    for line in lines[2:2 + n]:
        name, amount = line.split()
        paid[name] += int(amount) * 100
    return names, paid


def balances(names, paid):
    """Баланс участника: сколько потратил минус его доля.

    Если сумма не делится нацело, лишние копейки добавляются к доле тех,
    кто потратил меньше всех (они и так будут переводить деньги).
    """
    total = sum(paid.values())
    base, extra = divmod(total, len(names))
    share = {name: base for name in names}
    for name in sorted(names, key=lambda x: paid[x])[:extra]:
        share[name] += 1
    return {name: paid[name] - share[name] for name in names}


def exact_groups(people, bal):
    k = len(people)
    size = 1 << k
    sums = [0] * size
    for mask in range(1, size):
        low = mask & -mask
        sums[mask] = sums[mask ^ low] + bal[people[low.bit_length() - 1]]

    dp = [0] * size
    parent = [0] * size
    for mask in range(1, size):
        best = -1
        rest = mask
        while rest:
            bit = rest & -rest
            rest ^= bit
            if dp[mask ^ bit] > best:
                best = dp[mask ^ bit]
                parent[mask] = bit
        dp[mask] = best + (sums[mask] == 0)

    groups, current = [], []
    mask = size - 1
    while mask:
        if sums[mask] == 0 and current:
            groups.append(current)
            current = []
        bit = parent[mask]
        current.append(people[bit.bit_length() - 1])
        mask ^= bit
    if current:
        groups.append(current)
    return groups


def heuristic_groups(people, bal):
    """Выделяет пары с противоположными балансами, остальных объединяет в одну группу."""
    groups, rest = [], []
    waiting = {}
    for name in people:
        partner = waiting.get(-bal[name])
        if partner:
            groups.append([partner.pop(), name])
        else:
            waiting.setdefault(bal[name], []).append(name)
    for names in waiting.values():
        rest.extend(names)
    if rest:
        groups.append(rest)
    return groups


def settle(group, bal):
    """Жадно гасит долги внутри группы: k - 1 перевод на k участников."""
    debtors = [[name, -bal[name]] for name in group if bal[name] < 0]
    creditors = [[name, bal[name]] for name in group if bal[name] > 0]
    debtors.sort(key=lambda x: -x[1])
    creditors.sort(key=lambda x: -x[1])
    transfers = []
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        amount = min(debtors[i][1], creditors[j][1])
        transfers.append((debtors[i][0], creditors[j][0], amount))
        debtors[i][1] -= amount
        creditors[j][1] -= amount
        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1
    return transfers


def solve(names, paid):
    bal = balances(names, paid)
    people = [name for name in names if bal[name] != 0]
    if len(people) <= EXACT_LIMIT:
        groups = exact_groups(people, bal)
    else:
        groups = heuristic_groups(people, bal)
    transfers = []
    for group in groups:
        transfers.extend(settle(group, bal))
    return transfers


def main():
    names, paid = read_input(sys.stdin)
    transfers = solve(names, paid)
    print(len(transfers))
    for sender, receiver, amount in transfers:
        print(sender, receiver, fmt(amount))


if __name__ == "__main__":
    main()
