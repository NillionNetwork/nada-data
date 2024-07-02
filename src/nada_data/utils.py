

def next_power_of_two(n: int) -> int:
    """
    Determine the next power of 2 for some n

    >>> next_power_of_two(2)
    2
    >>> next_power_of_two(37)
    64
    >>> next_power_of_two(-10)
    1
    """

    if n <= 0:
        return 1

    p = 1
    while p < n:
        p <<= 1

    return p


if __name__ == "__main__":
    import doctest
    doctest.testmod()
