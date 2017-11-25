"""Numerical Methods"""

from math import *
from fractions import Fraction

def sign(x):
    if x == 0: return 0
    if x < 0: return -1
    return 1

def bisect(expression, interval, error=1e-4):
    """Attempts to find the zero of a function using the
    bisection method given a function, a number on each
    side of the number, and error (optional)."""

    [left_bound, right_bound] = interval

    f = expression

    if sign(f(left_bound)) == sign(f(right_bound)):
        raise ValueError('For the algorithm to work, the boundaries must have different signs (+/-).')

    midpoint = float((left_bound + right_bound) / 2)
    iteration = 0

    while abs(f(midpoint)) > error and iteration <= 4000:
        midpoint = float((left_bound + right_bound) / 2)
        mid_sign = sign(f(midpoint))

        if mid_sign == 0:
            return midpoint

        if sign(f(left_bound)) == mid_sign:
            left_bound = midpoint

        elif sign(f(right_bound)) == mid_sign:
            right_bound = midpoint

        iteration += 1

    return midpoint


def secant(expression, x0, x1):
    """Returns the slope of the secant line
    to the expression with respect to points
    x_0 and x_1."""

    f = expression

    return (f(x1) - f(x0)) / (x1 - x0)


def n_derive(expression, x0, error=1e-4):
    """Gives the approximate derivative of an
    expression at point x_0 using secants."""

    f = expression

    n = 0.1
    
    k = secant(expression, x0 - n, x0 + n) - secant(expression, x0 - n / 10, x0 + n / 10)
    iteration = 0
    while k > error and iteration <= 5000:
        n /= 10
        iteration += 1
        k = secant(expression, x0 - n, x0 + n) - secant(expression, x0 - n / 10, x0 + n / 10)

    return float(secant(expression, x0 - n, x0 + n))


def newton(expression, seed, error=1e-4):
    """Attempts to find the zero of a function using
    Newton's method given a function, a seed number,
    and error (optional)."""

    f = expression

    iteration = 0

    if f(seed) == 0: return seed

    while abs(f(seed)) / n_derive(expression, seed, error / 100) > error and iteration <= 4000:
        seed -= float(f(seed) / n_derive(expression, seed, error / 100))
        iteration += 1
    return seed - float(f(seed) / n_derive(expression, seed, error / 100))


def riemann(expression, interval, terms):
    
    f = expression

    [x0, x1] = interval
    ans = 0

    delta_x = (x1 - x0) / terms
    for k in range(terms):
        ans += f(x0 + (k + 1 / 2) * delta_x) * delta_x
    return ans
