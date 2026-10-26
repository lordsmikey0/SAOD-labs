#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 3. Простые сортировки и QuickSort с рандомизацией — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-03 и правилами использования генеративного ИИ
(docs/ai-verification.md).

Запуск: python lab03-simple-sorts-quicksort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import time

# ---------------------------------------------------------------------------
# 1. Простые сортировки со счётчиками (сортируют КОПИЮ входа, вход не меняют)
#    Каждая функция возвращает кортеж: (отсортированный список,
#    число сравнений ключей, число обменов/перемещений элементов).
# ---------------------------------------------------------------------------


def bubble_sort(a: list, key_fn = lambda x: x) -> tuple[list, int, int]:
    """
    Сортировка массива пузырьком с флагом досрочного выхода.
    Сложность: O(n^2)

    """
    array = a.copy()
    comparisons: int = 0
    exchanges: int = 0

    for i in range(len(array)):
        swapped = False

        for j in range(0, len(array) - i - 1):
            if key_fn(array[j]) > key_fn(array[j + 1]):
                array[j], array[j + 1] = array[j + 1], array[j]
                exchanges += 1
                swapped = True
            comparisons += 1

        if not swapped:
            break

    return array, comparisons, exchanges


def insertion_sort(a: list, key_fn = lambda x: x) -> tuple[list, int, int]:
    """
    Сортировка массива вставкой.

    Сложность:
    Лучший случай - O(n)
    Худший случай - O(n^2)

    """
    array = a.copy()
    comparisons: int = 0
    exchanges: int = 0

    for i in range(1, len(array)):
        key = array[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if key_fn(key) >= key_fn(array[j]):
                break

            array[j + 1] = array[j]
            exchanges += 1
            j -= 1

        array[j + 1] = key
        exchanges += 1

    return array, comparisons, exchanges


def selection_sort(a: list, key_fn = lambda x: x) -> tuple[list, int, int]:
    """Сортировка выбором. Ожидаемая сложность: O(n^2)"""

    array = a.copy()
    comparisons: int = 0
    exchanges: int = 0

    for i in range(len(array) - 1):
        min_index = i

        for j in range(i + 1, len(array)):
            comparisons += 1

            if key_fn(array[j]) < key_fn(array[min_index]):
                min_index = j

        if min_index != i:
            array[i], array[min_index] = array[min_index], array[i]
            exchanges += 1

    return array, comparisons, exchanges


# ---------------------------------------------------------------------------
# 2. QuickSort с рандомизированным опорным элементом
# ---------------------------------------------------------------------------


def quick_sort(a: list, rng: random.Random | None = None,  key_fn = lambda x: x) -> list:
    """QuickSort с выбором опорного через rng.randrange. Возвращает новый список.

    Ожидаемая сложность:

    В среднем: O(n log n)
    Худший случай: O(n^2)

    """
    if rng is None:
        rng = random.Random()

    array = a.copy()

    def sort(lo: int, hi: int) -> None:
        if hi - lo <= 1:
            return

        pivot_index = rng.randrange(lo, hi)
        pivot = array[pivot_index]

        array[pivot_index], array[hi - 1] = array[hi - 1], array[pivot_index]

        boundary = lo

        for j in range(lo, hi - 1):
            if key_fn(array[j]) < key_fn(pivot):
                array[boundary], array[j] = array[j], array[boundary]
                boundary += 1

        array[boundary], array[hi - 1] = array[hi - 1], array[boundary]

        sort(lo, boundary)
        sort(boundary + 1, hi)

    sort(0, len(array))
    return array


# ---------------------------------------------------------------------------
# 3. Демонстрация стабильности на парах (ключ, метка)
# ---------------------------------------------------------------------------


def conclusion_constructor(result, pairs: list,  func_name: str = "") -> None:
    """
    Конструктор выводов для stability_demo.

    Показывает, какая из сортировок стабильна, а какая - нет
    """

    standard: list = sorted(pairs, key=lambda x: x[0])

    print(f"{func_name}:\n-----\nresult: {result}", "порядок сохранен" if result == standard else "порядок нарушен", "\n")

def stability_demo() -> None:
    """Показать, какие из четырёх сортировок стабильны.

    План: взять массив пар (ключ, метка) с повторяющимися ключами, например
    [(2, "a"), (1, "b"), (2, "c"), (1, "d")], отсортировать каждой сортировкой
    по ключу (сравнение только по p[0]!) и напечатать порядок меток при равных
    ключах. Вывод о стабильности каждой сортировки включить в отчёт.
    """

    test_data: list = [
        [(1, "a"), (1, "b"), (2, "c"), (1, "d")],
        [(2, "a"), (2, "b"), (1, "c")],
        [(3, "c"), (3, "d"), (1, "a"), (2, "b")]
    ]

    algorithms = [
        bubble_sort,
        insertion_sort,
        selection_sort,
        quick_sort
    ]

    key_fn = lambda x: x[0]

    for pairs in test_data:
        for algorithm in algorithms:
            if algorithm != quick_sort:
                result, comparisons, exchanges = algorithm(pairs, key_fn)
            else:
                result = algorithm(pairs, key_fn=key_fn)

            conclusion_constructor(result, pairs, algorithm.__name__)

# ---------------------------------------------------------------------------
# 4. Классы входов (данные по варианту, детерминированно по seed)
# ---------------------------------------------------------------------------


def make_inputs(n: int, seed: int) -> dict[str, list[int]]:
    """Три класса входов размера n: упорядоченный, случайный, обратный."""
    rng = random.Random(seed + n)  # свой поток для каждого размера
    data = [rng.randint(-1_000_000, 1_000_000) for _ in range(n)]
    return {
        "упорядоченный": sorted(data),
        "случайный": data,
        "обратный": sorted(data, reverse=True),
    }


# ---------------------------------------------------------------------------
# 5. Верификация (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------

ALGORITHMS = {
    "bubble_sort": lambda a: bubble_sort(a)[0],
    "insertion_sort": lambda a: insertion_sort(a)[0],
    "selection_sort": lambda a: selection_sort(a)[0],
    "quick_sort": lambda a: quick_sort(a, random.Random(0)),
}


def is_sorted(a: list) -> bool:
    """Инвариант 1: неубывающий порядок элементов."""
    return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def self_check() -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [5, 5, 5, 5],          # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for name, fn in ALGORITHMS.items():
        for a in boundary:
            res = fn(list(a))
            assert is_sorted(res), f"{name}: нарушен порядок на {a}"
            assert sorted(res) == sorted(a), f"{name}: не перестановка входа {a}"

    # Сверка с эталоном из стандартной библиотеки на сотнях случайных входов.
    rng = random.Random(0)
    for _ in range(300):
        a = [rng.randint(-100, 100) for _ in range(rng.randint(0, 80))]
        expected = sorted(a)
        for name, fn in ALGORITHMS.items():
            assert fn(list(a)) == expected, f"{name}: расходится с sorted() на {a}"

    # Счётчики: у сортировки выбором ровно n*(n-1)/2 сравнений на любом входе.
    _, comparisons, _ = selection_sort([3, 1, 2, 5, 4])
    assert comparisons == 10, "selection_sort: неверный счётчик сравнений"
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 6. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES_QUADRATIC = [500, 1_000, 2_000, 4_000, 8_000]     # для простых сортировок
SIZES_QUICK = [1_000, 3_000, 10_000, 30_000, 100_000]   # для QuickSort
REPEATS = 5


def bench(fn, data: list) -> float:
    """Медиана времени выполнения fn(копия data) по REPEATS запускам, с прогревом."""
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        arg = list(data)  # свежая копия: сортировка не должна получать свой результат
        t0 = time.perf_counter()
        fn(arg)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    """Замеры всех алгоритмов на трёх классах входов; результат — таблица в stdout."""
    plans = [
        ("bubble_sort", ALGORITHMS["bubble_sort"], SIZES_QUADRATIC),
        ("insertion_sort", ALGORITHMS["insertion_sort"], SIZES_QUADRATIC),
        ("selection_sort", ALGORITHMS["selection_sort"], SIZES_QUADRATIC),
        ("quick_sort", lambda a: quick_sort(a, random.Random(seed)), SIZES_QUICK),
    ]
    for name, fn, sizes in plans:
        print(f"\n{name}:")
        for n in sizes:
            for cls, data in make_inputs(n, seed).items():
                print(f"  n={n:>7}  вход={cls:<13} t={bench(fn, data):.6f} c")
    # TODO: построить log-log графики (matplotlib) по классам входов;
    # TODO: сопоставить наклоны с O(n^2) и O(n log n), объяснить расхождения
    #       (в т. ч. лучший случай вставок и поведение пузырька на упорядоченном входе);
    # TODO: включить в отчёт таблицы счётчиков сравнений/обменов.


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    stability_demo()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
