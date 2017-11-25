from math import *
from statistics import *
import random
from num_methods import bisect
from matrix import *


def bell(x, sigma, mu):
    return 1 / (sigma * sqrt(2 * pi)) * exp(-(x - mu) ** 2 / (2 * sigma ** 2))


def normal(zscore):
    """Probability that a value lies
    between -oo and mu + sigma * zscore."""
    return abs(erf(zscore / sqrt(2)) / 2 + 0.5)


def inv_normal(probability, interval=None):
    if interval is None:
        interval = [-8, 8]
    return bisect(lambda x: normal(x) - probability, interval, 1e-12)


def birthday_problem(people, days=365, days_between=0):
    n = people
    m = days
    k = days_between
    
    return 1 - factorial(m - k * n - 1) / (m ** (n - 1) * factorial(m - n * (k + 1)))


def birthday_attack(probability_exponent, bits):
    """Estimates the number of randomly chosen values of a
    certain base (bits) needed to find a hash collision with
    the desired probability of 10 ** (probability_exponent).
    
    Relies on the Birthday Attack, see:
        https://en.wikipedia.org/wiki/Birthday_attack
    or
        https://en.wikipedia.org/wiki/Birthday_problem
    """
    probability = 10. ** probability_exponent
    outputs = 2. ** bits
    return sqrt(2. * outputs * -log1p(-probability))


def benford(n):
    """Returns log10(n + 1) - log10(n)
    
    A set of numbers is said to satisfy Benford's
    law if the leading digits n occurs with
    the probability log10(n + 1) - log10(n).
    
    For more information, see the wikipedia link:
        https://en.wikipedia.org/wiki/Benford%27s_law
    """

    if type(n) != int:
        raise ValueError('n must be a integer.')

    return log10(n + 1) - log10(n)


def benford2(n, digit=2):
    """Returns probablilty that digit (digit) in
    a integer string is equal to n.
    
    see benford.
    """

    if type(n) != int or n not in range(10):
        raise ValueError('n must be a integer between 0 and 9 inclusive.')

    if type(digit) != int or digit <= 1:
        raise ValueError('The digit must be a greater than 1.')

    ans = 0
    for k in range(10 ** (digit - 2), 10 ** (digit - 1)):
        ans += log10(1 + 1 / (10 * k + n))

    return ans

def pcovariance(X, Y):
    X_mu  = mean(X)
    Y_mu  = mean(Y)
    X     = [n - X_mu for n in X]
    Y     = [n - Y_mu for n in Y]
    total = [X[n] * Y[n] for n in range(min(len(X), len(Y)))]
    return mean(total)

def covariance(X, Y):
    return pcovariance(X, Y) * min(len(X), len(Y)) / (min(len(X), len(Y)) - 1)

def pcorrelation(X, Y):
    return pcovariance(X, Y) / (pstdev(X) * pstdev(Y))

def correlation(X, Y):
    return covariance(X, Y) / (stdev(X) * stdev(Y))
    
def line(X, Y):
    k = covariance(X, Y)/ variance(X)
    return [k, mean(Y) - k * mean(X)]

def pline(X, Y):
    k = pcorrelation(X, Y)/pvariance(X)
    return [k, mean(X) - k * mean(Y)]

def poly_reg(X, Y, m):
	poly_list = []
	if m >= len(X): raise ValueError("m must be less than len(X). (m < len(X))")
	for x in X:
		poly_list.append([x ** k for k in range(m + 1)])
	X_ = Matrix(*poly_list)
	Y_ = Matrix(*[[n] for n in Y])
	return ((X_.transpose() * X_)**-1 * X_.transpose() * Y_).columns[0]
    
def sample(n, trials, data):
    means = []
    for k in range(trials):
        means += [mean(random.choices(data, k=n))]
    print('Trials:          ' + str(trials))
    print('Sample Size (n): ' + str(n))
    print('-' * 35)
    print('mu:            ' + str(mean(data)))
    print('mu_xbar:       ' + str(mean(means)))
    print('sigma:         ' + str(pstdev(data)))
    print('SE_xbar:       ' + str(pstdev(means)))
    print('sigma/sqrt(n): ' + str(pstdev(data) / n ** 0.5))

def lin_reg():
    print('\n\nLine of Best Fit Calculator:\n' + '-' * 40 + '\n')
    X = input('Enter your X values separated by commas:\n>>> ')
    print()
    Y = input('Enter your Y values separated by commas:\n>>> ')
    print()
    X = [float(n) for n in X.split(',')]
    Y = [float(n) for n in Y.split(',')]
    print('Slope:     {}'.format(round(line(X, Y)[0], 6)))
    print('Intercept: {}'.format(round(line(X, Y)[1], 6)))
    print('Correlation (r): {}'.format(round(correlation(X, Y), 6)))

def exp_reg():
    print('\nExponential Regression Calculator:\n' + '-' * 40 + '\n')
    X = input('Enter your X values separated by commas:\n>>> ')
    print()
    Y = input('Enter your Y values separated by commas:\n>>> ')
    print()
    X = [float(n) for n in X.split(',')]
    Y = [log(float(n)) for n in Y.split(',')]
    b = line(X, Y)[0]
    a = line(X, Y)[1]
    print('Y ~ a * b ** X')
    print('a = {}'.format( round(exp(a), 6) ))
    print('b = {}'.format( round(exp(b), 6) ))
    print('Correlation (r): {}'.format(round(correlation(X, Y), 6)))
