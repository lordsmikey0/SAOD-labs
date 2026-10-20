import random

def bubble_sort(array: list) -> dict:
    """
    Сортировка массива пузырьком с флагом досрочного выхода.
    Сложность: O(n^2)

    """
    array = array.copy()
    comparisons: int = 0
    exchanges: int = 0

    for i in range(len(array)):
        swapped = False

        for j in range(0, len(array) - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                exchanges += 1
                swapped = True
            comparisons += 1

        if not swapped:
            break

    return {"array": array, "comparisons": comparisons, "exchanges": exchanges}


def insertion_sort(array: list) -> dict:
    """
    Сортировка массива вставкой.

    Сложность:
    Лучший случай - O(n)
    Худший случай - O(n^2)

    """
    array = array.copy()
    comparisons: int = 0
    exchanges: int = 0

    for i in range(1, len(array)):
        key = array[i]
        j = i - 1

        while j >= 0:
            comparisons += 1

            if key >= array[j]:
                break

            array[j + 1] = array[j]
            exchanges += 1
            j -= 1

        array[j + 1] = key
        exchanges += 1

    return {"array": array, "comparisons": comparisons, "exchanges": exchanges}


def selection_sort(array: list) -> dict:
    """Сортировка выбором. Ожидаемая сложность: O(n^2)"""

    array = array.copy()
    comparisons: int = 0
    exchanges: int = 0

    for i in range(len(array) - 1):
        min_index = i

        for j in range(i + 1, len(array)):
            comparisons += 1

            if array[j] < array[min_index]:
                min_index = j

        if min_index != i:
            array[i], array[min_index] = array[min_index], array[i]
            exchanges += 1

    return {"array": array, "comparisons": comparisons, "exchanges": exchanges}


def quick_sort(array: list, rng: random.Random | None = None) -> list:
    """QuickSort с выбором опорного через rng.randrange. Возвращает новый список.

    Ожидаемая сложность:

    В среднем: O(n log n)
    Худший случай: O(n^2)

    """
    if rng is None:
        rng = random.Random()

    array = array.copy()

    def sort(lo: int, hi: int) -> None:
        if hi - lo <= 1:
            return

        pivot_index = rng.randrange(lo, hi)
        pivot = array[pivot_index]

        array[pivot_index], array[hi - 1] = array[hi - 1], array[pivot_index]

        boundary = lo

        for j in range(lo, hi - 1):
            if array[j] < pivot:
                array[boundary], array[j] = array[j], array[boundary]
                boundary += 1

        array[boundary], array[hi - 1] = array[hi - 1], array[boundary]

        sort(lo, boundary)
        sort(boundary + 1, hi)

    sort(0, len(array))
    return array
