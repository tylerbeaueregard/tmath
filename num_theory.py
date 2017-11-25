from sympy.ntheory import primetest, generate, sieve
from math import *
from fractions import Fraction, gcd

isprime, p, primepi = primetest.isprime, generate.prime, generate.primepi


def factor(n):
    """"Lists all the factors of n"""
    
    factor_list = []
    l = list(range(1, 1 + int(ceil(sqrt(n)))))
    if n % 2 != 0:
        l = l[0::2]
    for a in l:
        if n % a == 0:
            factor_list += [a, n // a]
    return sorted(list(set(factor_list)))


def lcm(*args):
    if len(args) == 2:
        a, b = args[0], args[1]
        try:
            return int(Fraction(abs(a * b), gcd(a, b)))
        except TypeError:
            return abs(a * b) / gcd(a, b)
    else:
        args = [lcm(args[0], args[1])] + list(args)[2:]
        return lcm(*args)


def plist(n):
        """"list of primes up to nth prime inclusive"""
        return list(sieve.primerange(1, p(n) + 1))


def pfactorial(n):
    """nth prime multiplied by all desending primes- gives
    the lcm of all integers up to the nth prime."""
    
    if n == 1:
        return 2
    if n > 1:
        return p(n) * pfactorial(n - 1)



def pfactor(n):
    """Lists prime factorization of n.
    ex. 
    >>> pfactor(12)
    [2, 2, 3]
    """
    
    if isprime(n):
        return [n]
        
    factor_list = []
    '''for prime in plist(int(primepi(n)) + 1):
        while n % prime == 0:
            factor_list.append(prime)
            n = n // prime;'''
    for k in factor(n):
        if isprime(k):
            factor_list.append(k)
    return factor_list
    

def nextp(n):
    """"Gives next prime after integer n"""
    while isprime(n + 1) == 0:
        n = n + 1
    return n + 1
    

def lastp(n):
    """"Gives last prime before integer n"""
    while isprime(n - 1) == 0:
        n = n - 1
    return n - 1


def slist(top, index = False):
    """
    lists primes <= top such that
    the prime can be written as the
    sum of the first n consecutive primes.
    
    :type index: boolean object
    """
    summ = 0
    ans = []
    n = 1
    while summ+p(n) <= top:
        summ += p(n)
        if isprime(summ):
            if not index:
                ans.append(summ)
            else:
                ans.append([n, summ])
        n += 1
    if index:
        ans = dict(ans)
    return ans


def sigl(n):
    k = [0] + list(slist(n, True).values())
    j = []
    for m in range(len(k) - 1):
        j += [m] * (k[m+1] - k[m])
    m = len(k) - 2
    return j + [m+1] * (n - len(j) + 1)
