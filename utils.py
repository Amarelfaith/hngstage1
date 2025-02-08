import math


def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def is_perfect(n: int) -> bool:
    """Return True if n is a perfect number (i.e., sum of proper divisors equals n)."""
    if n < 1:
        return False
    sum_div = 1 if n > 1 else 0
    for i in range(2, int(n / 2) + 1):
        if n % i == 0:
            sum_div += i
    return sum_div == n


def is_armstrong(n: int) -> bool:
    """Return True if n is an Armstrong number."""

    digits = str(abs(n))
    num_digits = len(digits)
    armstrong_sum = sum(int(digit) ** num_digits for digit in digits)
    return armstrong_sum == abs(n)


def digit_sum(n: int) -> int:
    """Return the sum of the digits of n (ignoring the sign)."""
    return sum(int(d) for d in str(abs(n)))
