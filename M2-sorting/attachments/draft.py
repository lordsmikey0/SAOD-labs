import random


def merge(left: list, right: list, key) -> list:
    """
    Стабильное слияние двух отсортированных списков в новый список.

    Стабильность: при равенстве ключей элемент из left идёт раньше.
    Ожидаемая сложность: TODO (обосновать в отчёте).
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
    MergeSort: возвращает новый отсортированный список. Ожидаемая сложность: TODO.
    """
    if len(a) <= 1:
        return a.copy()

    mid = len(a) // 2

    left = merge_sort(a[:mid], key)
    right = merge_sort(a[mid:], key)

    return merge(left, right, key)


# --------------

def counting_sort(a: list[int], key_max: int) -> list[int]:
    """
    Устойчивая сортировка подсчётом: ключи — целые из диапазона [0, key_max].

    Схема: массив счётчиков -> префиксные суммы -> расстановка с конца.
    Ожидаемые время и память: TODO — выразить через n и k = key_max + 1;
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

print(counting_sort([3, 1, 2, 1, 3, 1], 3))

# --------------

def radix_sort_lsd(a: list[int]) -> list[int]:
    """
    RadixSort LSD по десятичным разрядам, неотрицательные целые.

    Поверх устойчивой поразрядной counting-сортировки: от младшего разряда
    к старшему. Ожидаемая сложность: TODO — выразить через n и число разрядов d.
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

# --------------

def sift_down(a: list[int], i: int, n: int) -> None:
    """Просейка вниз элемента i в куче a[0:n] (max-heap), на месте."""
    # TODO: спуск с обменом с большим из потомков, пока нарушено свойство кучи
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