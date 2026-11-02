#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Исправленный код. Исправление прошло строго после верификации

from __future__ import annotations
import random

def quicksort(data: list[int], rng: random.Random | None = None) -> list[int]:
    """
    Sort a list of integers using the quicksort algorithm.

        Efficient quicksort implementation based on the classic
        divide-and-conquer strategy. Expected time complexity: O(n log n);
        worst-case time complexity: O(n^2). Expected auxiliary space: O(n);
        worst-case auxiliary space: O(n^2) for retained partition lists.
        Recursion depth is O(log n) in expectation and O(n) in the worst case.
        The input list is not modified; a new sorted list is returned.
        Pass a seeded random.Random instance for reproducible pivot choices.
        If rng is omitted, the shared generator controlled by random.seed()
        is used.

        Examples
        --------
        >>> quicksort([3, 1, 2])
        [1, 2, 3]
        >>> quicksort([])
        []
    """

    if len(data) <= 1:
        return list(data)

    pivot = random.choice(data) if rng is None else rng.choice(data)

    smaller = [x for x in data if x < pivot]
    equal = [x for x in data if x == pivot]
    larger = [x for x in data if x > pivot]

    return quicksort(smaller, rng) + equal + quicksort(larger, rng)


if __name__ == "__main__":
    example = [5, 2, 9, 1, 7]
    print("Input :", example)
    print("Sorted:", quicksort(example))
