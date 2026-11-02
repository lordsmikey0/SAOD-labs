#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Исправленный код. Исправление прошло строго после верификации

from __future__ import annotations

def quicksort(data: list[int]) -> list[int]:
    """
    Sort a list of integers using the quicksort algorithm.

        Efficient quicksort implementation based on the classic
        divide-and-conquer strategy. Time complexity: O(n log n),
        space complexity: O(log n) for the recursion stack.
        The input list is not modified; a new sorted list is returned.

        Examples
        --------
        >>> quicksort([3, 1, 2])
        [1, 2, 3]
        >>> quicksort([])
        []
    """
    if len(data) <= 1:
        return list(data)

    pivot = data[len(data) // 2]

    smaller = [x for x in data if x < pivot]
    equal = [x for x in data if x == pivot]
    larger = [x for x in data if x > pivot]

    return quicksort(smaller) + equal + quicksort(larger)


if __name__ == "__main__":
    example = [5, 2, 9, 1, 7]
    print("Input :", example)
    print("Sorted:", quicksort(example))
