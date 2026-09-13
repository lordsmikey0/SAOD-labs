# LAB WORK 1

# TASK 1
def array_sum(a: list[int]) -> int:
    """Сумма элементов массива. Ожидаемая сложность: TODO (обосновать в отчёте)."""
    # TODO: реализовать циклом

    # Сложность: Q(N)

    if a is None:
        raise TypeError(f"array_sum excepts a list of integers. Got None instead")
    if not isinstance(a, list):
        raise TypeError(f"array_sum expects a list of integers. Got {type(a).__name__} instead")
    if not a:
        return 0

    a_length: int = len(a)
    arr_sum: int = 0

    for i in range(a_length):
        if not isinstance(a[i], int):
            raise TypeError(f"Element at index {i} is not an integer. Got {type(a[i]).__name__} instead")
        arr_sum += a[i]
    return arr_sum


# TASK 2
def array_max(a: list[int]) -> int:
    """Максимум массива (массив непуст). Ожидаемая сложность: TODO."""
    # TODO: реализовать циклом

    # Сложность: Q(N)

    if a is None:
        raise TypeError(f"array_sum excepts a list of integers. Got {type(a).__name__} instead.")
    if not isinstance(a, list):
        raise TypeError(f"array_sum expects a list of integers. Got {type(a).__name__} instead.")
    if not a:
        raise ValueError("Can't find maximum of an empty list.")

    a_length: int = len(a)
    max_value = a[0]

    for i in range(1, a_length):
        if not isinstance(a[i], int):
            raise TypeError(f"Element at index {i} is not an integer. Got {type(a[i]).__name__} instead.")
        if a[i] > max_value:
            max_value = a[i]
    return max_value


# TASK 3
def count_equal_pairs(a: list[int]) -> int:
    """Число пар (i, j), i < j, таких что a[i] == a[j]. Ожидаемая сложность: TODO."""
    # TODO: реализовать двойным циклом

    # Сложность: Q(N^2)

    if a is None:
        raise TypeError(f"count_equal_pairs excepts a list of integers. Got None instead")
    if not isinstance(a, list):
        raise TypeError(f"array_sum expects a list of integers. Got {type(a).__name__} instead")
    if not a:
        return 0

    a_length: int = len(a)
    counter: int = 0

    for i in range(a_length):
        if not isinstance(a[i], int):
            raise TypeError(f"Element at index {i} is not an integer. Got {type(a[i]).__name__} instead.")
        for j in range(i + 1, a_length):
            if not isinstance(a[j], int):
                raise TypeError(f"Element at index {j} is not an integer. Got {type(a[j]).__name__} instead.")
            if a[i] == a[j]:
                counter += 1
    return counter


# TASK 4
def binary_pow(x: int, n: int, mod: int | None = None) -> int:
    """Бинарное возведение в степень, n >= 0. Ожидаемая сложность: TODO.

    При заданном mod все умножения выполняются по модулю (результат x**n % mod).
    """
    # TODO: реализовать через квадрирование; при mod применять % mod после
    # каждого умножения

    # Сложность O(log N)
    if x is None or n is None:
        raise TypeError(f"binary_pow expects 2 necessary variables - x and n as integers")
    if n < 0:
        raise ValueError(f"binary_pow expects n >= 0. Got {n} instead")
    if not isinstance(x, int) or not isinstance(n, int):
        raise TypeError(f"binary_pow got a wrong variable type. Everything should be int:"
                        f"x type:{type(x).__name__}, n type:{type(n).__name__}")

    result: int = 1

    while n > 0:
        if n % 2 == 1:
            result *= x
            if mod is not None:
                result %= mod
        x *= x
        if mod is not None:
            x %= mod
        n //= 2

    return result