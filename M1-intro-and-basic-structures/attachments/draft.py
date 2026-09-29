# TASK 1

def factorial(n: int) -> int:
    """Факториал n >= 0 рекурсивно. Ожидаемая сложность: TODO (обосновать в отчёте)."""
    if not isinstance(n, int):
        raise TypeError(f"[ERROR]: n should be int, got {type(n).__name__} instead")
    if n < 0:
        raise ValueError("[ERROR]: n should be >= 0")

    if n == 0:
        return 1
    return n * factorial(n - 1)


# TASK 2

def fib_naive(n: int) -> int:
    """n-е число Фибоначчи наивной рекурсией; увеличивает CALLS["fib_naive"].

    Ожидаемая сложность: TODO (экспоненциальная — показать счётчиком вызовов).
    """
    # CALLS["fib_naive"] += 1
    # TODO: F(0)=0, F(1)=1, далее F(n)=F(n-1)+F(n-2)
    if n in [0, 1]:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


# TASK 3

def fib_memo(n: int, memo: dict[int, int] | None = None) -> int:
    """n-е число Фибоначчи с мемоизацией; увеличивает CALLS["fib_memo"].

    Ожидаемая сложность: TODO (линейная — сравнить счётчики в отчёте).
    """
    # CALLS["fib_memo"] += 1
    # TODO: словарь memo передаётся по рекурсии; повторные подзадачи не пересчитываются
    if memo is None:
        memo = dict()

    print(memo)
    if n in memo:
        return memo[n]

    if n in [0, 1]:
        return n

    result = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    memo[n] = result
    return result


# TASK 4

def hanoi(n: int, src: str = "A", dst: str = "C", aux: str = "B",
          moves: list[tuple[str, str]] | None = None) -> int:
    """Ханойские башни: перенести n дисков со стержня src на dst, вернуть число перемещений.

    Если передан список moves, каждое перемещение верхнего диска дописывается
    в него парой (откуда, куда). self_check проигрывает эти ходы и проверяет,
    что больший диск ни разу не кладётся на меньший, все диски оказываются
    на dst, а число перемещений равно 2**n - 1.

    SRC - ОТКУДА (A)
    AUX - ВСПОМОГАТЕЛЬНОЕ (B)
    DST - КУДА (C)
    """

    if n == 0:
        return 0

    result1 = hanoi(n - 1, src, aux, dst, moves)

    if isinstance(moves, list):
        moves.append((src, dst))

    result2 = hanoi(n - 1, aux, dst, src, moves)

    return result1 + 1 + result2


# DynamicArray

class DynamicArray:
    """Динамический массив поверх «сырого» буфера фиксированной ёмкости.

    Инвариант: 0 <= self._size <= self._capacity.
    Буфер имитируем списком фиксированной длины, заполненным None;
    использовать list.append/insert/pop для буфера запрещено.
    """

    INITIAL_CAPACITY = 4

    def __init__(self) -> None:
        self._capacity = self.INITIAL_CAPACITY
        self._size = 0
        self._buffer: list = [None] * self._capacity  # «сырая» память
        self.copies = 0  # сколько элементов перенесено при смене буфера (метод учёта)

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return self._capacity

    def _grow(self) -> None:
        """Увеличить ёмкость в 2 раза и скопировать элементы в новый буфер."""

        self._capacity *= 2
        new_buffer: list = [None] * self.capacity

        for i in range(self._size):
            new_buffer[i] = self._buffer[i]

        self.copies += self._size
        self._buffer = new_buffer


    def append(self, value) -> None:
        """Добавить элемент в конец; при size == capacity сначала вызвать _grow.

        Амортизированная сложность: TODO (обосновать методом учёта в отчёте).
        """

        if self._size == self._capacity:
            self._grow()

        self._buffer[self._size] = value
        self._size += 1

    def pop(self):
        """Удалить и вернуть последний элемент; для пустого массива — IndexError.

        Сжатие буфера необязательно. Если реализуете его, уменьшайте ёмкость
        вдвое, когда size опускается до capacity // 4, и не ниже
        INITIAL_CAPACITY (перенесённые элементы тоже учитываются в copies):
        сжатие уже при заполнении на ½ даёт Θ(n) на операцию, если чередовать
        append и pop на границе ёмкости.
        """

        if self._size == 0:
            raise IndexError("pop from an empty array")

        # (None — чтобы буфер не удерживал объект), декремент _size

        value = self._buffer[self._size - 1]
        self._buffer[self._size - 1] = None
        self._size -= 1

        return value

    def get(self, index: int):
        """Вернуть элемент по индексу 0 <= index < size; иначе IndexError."""

        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        return self._buffer[index]

    def set(self, index: int, value) -> None:
        """Записать элемент по индексу 0 <= index < size; иначе IndexError."""

        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        self._buffer[index] = value