"""Tmath: math functions I 
use from time to time."""

from . import depend
from math import *
from fractions import Fraction, gcd
from itertools import permutations
from sympy import (acot, acsc, asec, asech, Chi,
 Ci, cot, csc, Derivative, dirichlet_eta, E, Ei,
 EulerGamma, exp_polar, expand, factor as fact,
 GoldenRatio, I, init_printing, Integral, LambertW,
 Li, li, Limit, ln, oo, pi as Pi, polygamma,
 polylog, pprint, sec, sech, Shi, Si, sieve, sign,
 simplify, solve, Symbol, symbols, sympify)

phi, i = float(GoldenRatio), 1j

def nPr(a, b):
    "Permutation of a and b"
    if a >= b:
        return factorial(a)//factorial(a - b)
    else:
        return 0


def nCr(a, b):
    """Combination a choose b"""
    if a >= b:
        return factorial(a)//(factorial(b)*factorial(a-b))
    else:
        return 0


def binomial_coef(n):
    """lists nth row of Pascal's triangle-
    coefficients of (x + y) **  n"""
    
    result = []
    for k in range(n + 1):
        p = nCr(n, k)
        result.append(p)
    return result


def pascal(n):
    """prints Pascal's triangle to nth row"""
    
    for row in range(n):
        for k in range(row + 1): 
            element = nCr(row, k)
            print(element, end = ' ')
        print()


def rad2deg(theta):
    return theta * 180 / pi


def deg2rad(theta):
    return theta * pi / 180


def tetrate(a, b):
    """Returns b iterations of a ** a
    (b must be a positive integer)
    This function grows rapidly.
    ex.
    >> tetrate(2, 3):
    16
    """
    if int(b) != b or b <= 0:
        raise ValueError('b must be a positive integer.')
    
    if b == 1:
        return a
    
    ans = a
    for n in range(b - 1):
        ans = a ** ans
    return ans


def superroot(x, iterations = 10 ** 4):
    """Returns n such that n ** n = y.
    x must be greater that 0.692"""
    ans = sqrt(x)
    try:
        for n in range(iterations):
            ans = sqrt(ans * x ** (1/ans))
        return ans
    except ZeroDivisionError:
        raise ValueError('x must be greater that 0.692')

def fibonacci(n):
    """Returns the nth Fibonacci number."""
    
    if n in [0, 1]:
        return n
    
    return fibonacci(n - 1) + fibonacci(n - 2)
