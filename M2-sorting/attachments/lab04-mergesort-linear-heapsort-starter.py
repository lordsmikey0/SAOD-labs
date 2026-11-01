#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ЛР 4. MergeSort, Counting, Radix и HeapSort: оценка производительности — стартовая заготовка.

Заготовка — это каркас, а не решение: заполните все TODO самостоятельно
в соответствии с КИМ-04 и правилами использования генеративного ИИ
(docs/ai-verification.md). QuickSort перенесите из собственной ЛР 3.

Запуск: python lab04-mergesort-linear-heapsort-starter.py --variant N
"""
from __future__ import annotations

import argparse
import random
import statistics
import sys
import time
import traceback
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Сортировки (реализуются вручную; sorted() используется только как эталон)
# ---------------------------------------------------------------------------


def merge(left: list, right: list, key) -> list:
    """
    Стабильное слияние двух отсортированных списков в новый список.

    Стабильность: при равенстве ключей элемент из left идёт раньше.
    Ожидаемая сложность: O(n).
    """
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def merge_sort(a, key=lambda x: x):
    """
    MergeSort: возвращает новый отсортированный список. Ожидаемая сложность: O(n log n).
    """
    if len(a) <= 1:
        return a.copy()

    mid = len(a) // 2

    left = merge_sort(a[:mid], key)
    right = merge_sort(a[mid:], key)

    return merge(left, right, key)


def counting_sort(a: list[int], key_max: int) -> list[int]:
    """
    Устойчивая сортировка подсчётом: ключи — целые из диапазона [0, key_max].

    Схема: массив счётчиков -> префиксные суммы -> расстановка с конца.
    Ожидаемые время и память: O(n + k).
    ограничение диапазона ключей обсудить в отчёте.
    """
    result: list[int] = [0] * len(a)
    counts: list[int] = [0] * (key_max + 1)

    for element in a:
        counts[element] += 1

    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]

    for element in reversed(a):
        position = counts[element] - 1
        result[position] = element
        counts[element] -= 1

    return result


def radix_sort_lsd(a: list[int]) -> list[int]:
    """
    RadixSort LSD по десятичным разрядам, неотрицательные целые.

    Поверх устойчивой поразрядной counting-сортировки: от младшего разряда
    к старшему. Ожидаемая сложность: O(dn)
    """
    if len(a) == 0:
        return []

    max_value = max(a)
    exp = 1

    while exp <= max_value:
        counts = [0] * 10
        result = [0] * len(a)

        for element in a:
            digit = element // exp % 10
            counts[digit] += 1

        for i in range(1, len(counts)):
            counts[i] += counts[i - 1]

        for element in reversed(a):
            digit = element // exp % 10
            position = counts[digit] - 1
            result[position] = element
            counts[digit] -= 1

        a = result
        exp *= 10

    return a


def sift_down(a: list[int], i: int, n: int) -> None:
    """
    Просейка вниз элемента i в куче a[0:n] (max-heap), на месте.

    Сложность: O(log n)
    """
    while True:
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        if left < n and a[left] > a[largest]:
            largest = left
        if right < n and a[right] > a[largest]:
            largest = right
        if largest == i:
            break

        a[i], a[largest] = a[largest], a[i]
        i = largest


def heap_sort(a: list[int]) -> None:
    """
    HeapSort in-place: сортирует список a на месте, без вспомогательного массива.

    Схема: построение max-кучи просейками вниз (снизу вверх, O(n)),
    затем обмен вершины с последним элементом и просейка. Сложность: O(n log n).

    """
    n = len(a)

    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)

    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        sift_down(a, 0, end)


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

        pivot = key_fn(array[rng.randrange(lo, hi)])

        lt = lo
        i = lo
        gt = hi

        while i < gt:
            value = key_fn(array[i])

            if value < pivot:
                array[lt], array[i] = array[i], array[lt]
                lt += 1
                i += 1
            elif value > pivot:
                gt -= 1
                array[i], array[gt] = array[gt], array[i]
            else:
                i += 1

        sort(lo, lt)
        sort(gt, hi)

    sort(0, len(array))
    return array


# ---------------------------------------------------------------------------
# 2. Верификация: инварианты + сверка с эталоном sorted()
#    (шаги 1–3 методики docs/ai-verification.md)
# ---------------------------------------------------------------------------


class SelfCheckError(Exception):
    """Нарушен контракт или инвариант реализации."""


def expect(condition: bool, message: str) -> None:
    """Явная проверка вместо assert: assert-ы исчезают при запуске python -O."""
    if not condition:
        raise SelfCheckError(message)


def heap_sorted(a: list[int]) -> list[int]:
    """heap_sort сортирует на месте: проверяется тот список, который ему передали."""
    buf = list(a)
    heap_sort(buf)
    return buf


# Каждая функция возвращает отсортированный список; ключи — целые из [0, 999].
SORTS = {
    "merge_sort": lambda a: merge_sort(a),
    "counting_sort": lambda a: counting_sort(a, key_max=999),
    "radix_sort_lsd": lambda a: radix_sort_lsd(a),
    "heap_sort": lambda a: heap_sorted(a),
    "quick_sort": lambda a: quick_sort(a),
}


def check_sort(fn) -> None:
    """Граничные случаи, инварианты сортировки и сверка с эталоном sorted()."""
    boundary = [
        [],                    # пустой массив
        [7],                   # один элемент
        [0],                   # нулевой ключ
        [5, 5, 5],             # все элементы равны
        [1, 2, 3, 4, 5],       # уже отсортирован
        [5, 4, 3, 2, 1],       # обратный порядок
    ]
    for a in boundary:
        res = fn(list(a))
        expect(isinstance(res, list), f"на {a} возвращён {type(res).__name__}, а не список")
        expect(res == sorted(a), f"на {a} получено {res}, ожидалось {sorted(a)}")

    # Случайные тесты: инвариант перестановки + сверка с эталоном
    rng = random.Random(0)
    for _ in range(200):
        a = [rng.randint(0, 999) for _ in range(rng.randint(0, 60))]
        res = fn(list(a))
        expect(sorted(res) == sorted(a), f"не перестановка входа {a}: получено {res}")
        expect(res == sorted(a), f"расходится с sorted() на {a}: получено {res}")


def check_merge_stability() -> None:
    """Стабильность слияния на парах (ключ, порядковый номер): эталон sorted() стабилен,
    поэтому при равных ключах порядок номеров обязан совпасть."""
    rng = random.Random(0)
    pairs = [(rng.randint(0, 5), i) for i in range(100)]
    got = merge_sort(pairs, key=lambda p: p[0])
    expect(got == sorted(pairs, key=lambda p: p[0]),
           "merge_sort нестабилен: при равных ключах нарушен исходный порядок номеров")


def check_heap_property() -> None:
    """Проверяет свойство max-кучи после её построения."""
    a = [2, 9, 7, 5, 3, 1]
    n = len(a)

    for i in range(n // 2 - 1, -1, -1):
        sift_down(a, i, n)

    for i in range(n):
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n:
            expect(a[i] >= a[left], f"Нарушено свойство кучи: {a[i]} < {a[left]}")

        if right < n:
            expect(a[i] >= a[right], f"Нарушено свойство кучи: {a[i]} < {a[right]}")


def check_radix_stability() -> None:
    """Проверяет устойчивость одного поразрядного прохода."""

    class TaggedInt(int):
        def __new__(cls, value, tag):
            obj = super().__new__(cls, value)
            obj.tag = tag
            return obj

    a = [
        TaggedInt(2, "A"),
        TaggedInt(1, "B"),
        TaggedInt(2, "C"),
        TaggedInt(1, "D"),
    ]

    result = radix_sort_lsd(a)

    tags = [element.tag for element in result]

    expect(
        tags == ["B", "D", "A", "C"],
        f"Нарушена устойчивость RadixSort: {tags}"
    )


def self_check() -> None:
    """Все проверки по разделам; при любой ошибке замеры не выполняются."""
    # fn=fn фиксирует функцию текущего шага цикла (иначе все лямбды увидят последнюю)
    checks = [(name, lambda fn=fn: check_sort(fn)) for name, fn in SORTS.items()]

    checks.append(("стабильность merge_sort", check_merge_stability))
    checks.append(("свойство max-кучи", check_heap_property))
    checks.append(("устойчивость radix", check_radix_stability))

    failed = 0
    print("self_check:")
    for name, check in checks:
        try:
            check()
        except NotImplementedError as err:
            where = traceback.extract_tb(err.__traceback__)[-1].name
            print(f"  {name}: не реализовано — {where} (TODO)")
            failed += 1
        except SelfCheckError as err:
            print(f"  {name}: ОШИБКА — {err}")
            failed += 1
        except Exception:  # noqa: BLE001 — падение реализации тоже результат проверки
            print(f"  {name}: ИСКЛЮЧЕНИЕ")
            traceback.print_exc(file=sys.stdout)
            failed += 1
        else:
            print(f"  {name}: OK")
    # TODO: добавить собственные проверки (свойство кучи после построения,
    #       устойчивость поразрядного прохода radix) и описать их в отчёте.
    if failed:
        raise SystemExit(f"self_check: не пройдено разделов — {failed}; "
                         f"замеры выполняются только после всех проверок.")
    print("self_check: OK")


# ---------------------------------------------------------------------------
# 3. Бенчмарк (методика — docs/reproducibility.md)
# ---------------------------------------------------------------------------

SIZES = [1_000, 3_000, 10_000, 30_000, 100_000]
REPEATS = 5
SMALL_KEY_MAX = 100        # узкий диапазон: counting уместен
WIDE_KEY_MAX = 10**9       # широкий диапазон: counting теряет смысл (обсудить в отчёте)


def make_datasets(rng: random.Random, n: int) -> dict[str, list[int]]:
    """Массивы разных распределений и диапазонов ключей для размера n."""
    almost = list(range(n))
    for _ in range(max(1, n // 100)):  # ~1 % случайных обменов
        i, j = rng.randrange(n), rng.randrange(n)
        almost[i], almost[j] = almost[j], almost[i]
    return {
        "random_wide": [rng.randint(0, WIDE_KEY_MAX) for _ in range(n)],
        "random_small": [rng.randint(0, SMALL_KEY_MAX) for _ in range(n)],
        "sorted": list(range(n)),
        "reversed": list(range(n, 0, -1)),
        "almost_sorted": almost,
    }


def bench(fn, data: list[int]) -> float:
    """Медиана времени fn на копии data по REPEATS запускам, с прогревом.

    Каждый запуск получает свежую копию: сортировка на месте не должна
    превращать последующие запуски в сортировку уже отсортированного массива.
    """
    fn(list(data))  # прогрев — не учитывается
    times = []
    for _ in range(REPEATS):
        buf = list(data)
        t0 = time.perf_counter()
        fn(buf)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


def run_benchmarks(seed: int) -> None:
    rng = random.Random(seed)
    algorithms = [
        ("merge_sort", merge_sort),
        ("counting_sort", lambda a: counting_sort(a, key_max=max(a, default=0))),
        ("radix_sort_lsd", radix_sort_lsd),
        ("heap_sort", heap_sort),
        ("quick_sort (ЛР 3)", quick_sort),
        ("sorted() (эталон)", sorted),
    ]
    results = {}
    for n in SIZES:
        datasets = make_datasets(rng, n)
        print(f"\nn = {n}:")
        for dist_name, data in datasets.items():
            print(f"  распределение {dist_name}:")
            for algo_name, fn in algorithms:
                if algo_name == "counting_sort" and dist_name == "random_wide":
                    # счётчики размера ~10^9 не помещаются в память — граница
                    # применимости counting; зафиксировать в таблице свойств
                    print(f"    {algo_name:>18}: пропуск (диапазон ключей)")
                    continue
                elapsed = bench(fn, data)

                results.setdefault(algo_name, {}).setdefault(dist_name, []).append(
                    (n, elapsed)
                )

                print(f"    {algo_name:>18}: t = {elapsed:.6f} c")

    plot_results(results, Path("graphs"))

    # TODO: построить log-log графики (matplotlib) по каждому распределению;
    # TODO: заполнить таблицу свойств: время (лучший/средний/худший),
    #       память, стабильность, ограничения — для всех шести сортировок;
    # TODO: объяснить расхождения замеров с асимптотикой в отчёте.


# ---------------------------------------------------------------------------
# 4. Графики
# ---------------------------------------------------------------------------

def plot_results(results: dict, out_dir: Path) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib не установлен")
        return

    out_dir.mkdir(parents=True, exist_ok=True)

    for cls in [
        "random_wide",
        "random_small",
        "sorted",
        "reversed",
        "almost_sorted",
    ]:
        fig, ax = plt.subplots(figsize=(7, 5))

        for name, data in results.items():
            points = data.get(cls, [])
            if not points:
                continue

            ns = [n for n, t in points]
            ts = [t for n, t in points]

            ax.plot(ns, ts, marker="o", label=name)

        ax.set_xscale("log")
        ax.set_yscale("log")

        ax.set_xlabel("Размер массива n")
        ax.set_ylabel("Время, с")
        ax.set_title(f"Время сортировки: {cls} вход")

        ax.grid(True, which="both", linewidth=0.3)
        ax.legend()

        fig.tight_layout()

        path = out_dir / f"lab04_{cls}.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)

        print(f"График сохранён: {path}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--variant", type=int, required=True, help="номер варианта")
    args = ap.parse_args()
    seed = 30 + args.variant
    random.seed(seed)
    self_check()
    run_benchmarks(seed)


if __name__ == "__main__":
    main()
