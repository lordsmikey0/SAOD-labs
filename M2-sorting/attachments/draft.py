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
    Лучший случай - O
    Худший случай - O

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
    """Сортировка выбором. Ожидаемая сложность: TODO потом определю"""

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

