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

    return { "array": array, "comparisons": comparisons, "exchanges": exchanges}
