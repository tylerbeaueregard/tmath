from stats import *
from matplotlib import pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

def show(X = None, Y = None):
    
    print('Regression Calculator: ' + '\n' + '-' * 40)
    
    if not X:
        X = input('Enter your X values separated by commas:\n>>> ').split(',')
        print()
    if not Y:
        Y = input('Enter your Y values separated by commas:\n>>> ').split(',')
        print()
    
    X = [float(n) for n in X]
    Y = [float(n) for n in Y]
    
    type = input('Type: ')
    
    if type.lower() in ['exp', 'exponential']:
        n = float(input('n: '))
        x = X
        y = [log(n) for n in Y]
        [m, b] = line(x, y)
        line_x = [min(x) + n * (max(x) - min(x)) for n in range(ceil((max(x) - min(x))/n))]
        line_y = [exp(m * n + b) for n in line_x]

    else:
        x = X
        y = Y
        [m, b] = line(x, y)
        line_x = [min(x), max(x)]
        line_y = [m * n + b for n in line_x]
    
    title = input('Title: ')
    x_lb  = input('X Label: ')
    y_lb  = input('Y Label: ')
    dataA = input('Data Apperance: ')
    lineA = input('Line Color: ')[0]
    
    data = plt.plot(X, Y, dataA)
    lin = plt.plot(line_x, line_y, lineA, label = 'Regression Line\nSlope: {}\nIntercept: {}'.format(round(m, 6), round(b, 6)))
    
    plt.title(title)
    plt.xlabel(x_lb)
    plt.ylabel(y_lb)
    
    plt.legend()
    
    plt.show()
