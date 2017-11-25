"""General"""

from fractions import Fraction, gcd
from random import randint
import time

def gcds(*args):
    if len(args) == 1:
        return args[0]
    if len(args) == 2:
        return gcd(*args)
    return gcd(gcd(args[0], args[1]), gcds(*args[2:]))

class Matrix:

    def __init__(self, *rows):
        self.rows = list(rows)
        for n in rows:
            if len(n) != len(rows[0]):
                raise ValueError('Rows must be of same length.')
        self.columns = []
        for k in range(len(rows[0])):
            self.columns.append([n[k] for n in rows])
    
    def __eq__(self, mat):
        try:
            return mat.rows == self.rows
        except AttributeError:
            return False
    
    def __repr__(self):
        return '<Matrix object stored at location {}>'.format(id(self))
    
    def __str__(self):
        ans = ''
        lengths = []
        
        for n in self.columns:
            lengths.append(max([len(str(k)) for k in n]))
        
        for n in self.rows:
            ans += '['
            for k in range(len(n)):
                space = (lengths[k] - len(str(n[k]))) * ' '
                ans += space + str(n[k]) + ', '
            ans = ans[:-2]
            ans += ']\n'
        ans = ans[:-1]
        return ans

    def __list__(self):
        return self.rows
    
    def __add__(self, mat):
        if (len(self.rows), len(self.columns)) != (len(mat.rows), len(mat.columns)):
            raise ValueError('Matrix addition requires both matrices to have the same dimensions.')
        return Matrix(*[[self[k][n] + mat[k][n] for n in range(len(self.columns))] for k in range(len(self.rows))])
    
    def __mul__(self, factor):
        if type(factor) == type(self):
            if len(self.columns) != len(factor.rows):
                raise ValueError(
                    "For two matrices to be multiplied, the number of columns on matrix A"
                    " must equal the number of rows on matrix B"
                    )

            if len(self.rows) == 1:
                return Matrix([sum([self.rows[0][n] * factor.rows[n][0] for n in range(len(self.columns))])])

            ans = [[0 for n in range(len(factor.columns))] for k in range(len(self.rows))]
            
            for n in range(len(self.rows)):
                for k in range(len(factor.columns)):
                    ans[n][k] = (Matrix(self.rows[n]) * Matrix(*[[elem] for elem in factor.columns[k]]))[0][0]

            return Matrix(*ans)
            
        else:
            return Matrix(*[[self[k][n] * factor for n in range(len(self.columns))] for k in range(len(self.rows))])
    
    __rmul__ = __mul__

    def __truediv__(self, divisor):
        if type(divisor) == int:
            return self * Fraction(1, divisor)

        return self * (1 / divisor)

    def __rtruediv__(self, dividend):
        return dividend * self.inverse()

    def __pow__(self, power):
        if type(power) != int:
            raise ValueError("The 'Matrix' class currently only supports integer powers (not '{}').".format(type(power)))

        if power < 0:
            return self.inverse() ** (- power)

        ans = self.identity()

        for n in range(power):
            ans *= self

        return ans
    
    def __getitem__(self, key):
        return self.rows[key]
    
    def dim(self):
        return len(self.rows), len(self.columns)

    def identity(self):
        if not self.is_square():
            raise ValueError('Only square matrices can have a corresponding identity matrix')

        size = range(len(self.rows))
        
        ans = [[ 1 * (k == n) for k in size] for n in size]
        #Here 0 + (k == n) returns 1 if we are the matrix diagonal

        return Matrix(*ans)

    def is_square(self):
        for n in self.rows:
            if not len(n) == len(self.rows):
                return False
        return True

    def transpose(self):
        return Matrix(*self.columns)

    def cofactorn(self, row, column, tri = 1):
        mat = Matrix(*(self.rows[0:row] + self.rows[row + 1:]))
        mat = Matrix(*(mat.columns[0:column] + mat.columns[column + 1:])).transpose()
        return (-1)**(row + column) * mat.determinant(tri)

    def cofactor(self, tri = 1):
        ans = []
        for n in range(len(self.rows)):
            partial = []
            for k in range(len(self.columns)):
                partial.append(self.cofactorn(n, k, tri))
            ans.append(partial)
        return Matrix(*ans)

    def inverse(self, tri = 1):
        return self.cofactor(tri).transpose() / self.determinant(tri)

    def determinant(self, tri = 1):
    
        if not self.is_square():
            raise ValueError('Only square matrices have determinants.')
        
        if self.is_triangular():
            ans = 1
            diagonal = [self[k][k] for k in range(len(self.rows))]
            for k in diagonal:
                ans *= k
            
            return ans
        
        if tri: return self.triangular_det()

        ###This is the naive method### (I keep it around to test the other method.)
        for n in self.rows + self.columns:
            if set(n) == {0}:
                return 0
        
        if len(self.rows) == 1:
            return self[0][0]
        
        ans = 0
        for n in range(len(self[0])):
            partial = [self.rows[k][:n] + self.rows[k][n + 1:] for k in range(1, len(self.rows))]
            ans += (-1)**n * self[0][n] * Matrix(*partial).determinant(0)
        
        return ans
    
    def concat(self, mat):
        if len(self.rows) != len(mat.rows):
            raise ValueError('Both Matrices must have the same number of rows')
        
        ans = [0 for k in self.rows]
        
        for n in range(len(ans)):
            ans[n] = self.rows[n] + mat.rows[n]
        
        return Matrix(*ans)
    
    def triangular_det(self):
        
        if not self.is_square():
            raise ValueError('The matrix must be square.')
        
        if self.is_triangular():
            return self
        
        a = Matrix(*[n for n in self.rows]).transpose().transpose()
        n = len(a.rows)

        ###Dealing with fractions###
        has_fraction = False
        ff = 1
        
        for h in self.rows:
            for k in h:
                if type(k) != int:
                    if int(k) == k:
                        k = int(k)
                    else:
                        has_fraction = True
                        break

        if has_fraction:
            den = []
            for h in self.rows:
                partial = []
                for k in h:
                    frac = Fraction(k, 1)
                    partial.append(Fraction(1, frac.denominator))
                den.append(gcds(*partial))
            ff = int(Fraction(1, gcds(*den)))
            den = ff * a
            a = den.transpose().transpose()
        
        ####Now for the actual algorithm###
        uf = 1
        for j in range(n - 1):
            if a[j][j] == 0:
                for l in range(j + 1, n):
                    if a[l][j] != 0:
                        a.rows[j], a.rows[l] = a.rows[l], a.rows[j]
                        a = Matrix(*a)
                        uf *= -1
                if a[j][j] == 0:
                    return 0
            for i in range(j + 1, n):
                if a[i][j] != 0:
                    d = gcd(a[j][j], a[i][j])
                    b, c = a[j][j]//d , a[i][j]//d
                    uf *= b
                    for k in range(j + 1, n):
                        a[i][k] = b * a[i][k] - c * a[j][k]
                        
        ans = 1
        for k in range(n):
            ans *= a[k][k]

        if has_fraction:
            ans = ans//uf * Fraction(1, ff) ** n
            if int(ans) == ans: return int(ans)
            return ans
        return ans//uf
    
    def is_triangular(self):

        if not self.is_square():
            return False
        
        if len(self.rows) == 1:
            return True
        
        for k in range(len(self.rows)):
            if not self.rows[k][:k] == [0] * k:
                return False
        
        return True

def det(mat):
    return mat.determinant()

determinant = det

def inverse(mat):
    return mat.inverse()

def transpose(mat):
    return mat.transpose()

def random(rows, columns = None, lower = -50, upper = 50, fraction = False):
    if columns == None:
        columns = rows
    ans = [[randint(lower, upper) for k in range(columns)] for n in range(rows)]
    if fraction: ans = [[Fraction(k, randint(1, upper)) for k in n] for n in ans]
    return Matrix(*ans)


def identity(n):
    if type(n) == int:
        return Matrix(*[[1 * (j == k) for j in range(n)] for k in range(n)])
    
    else:
        return n.identity()

def timeit(size):
    a = time.time()
    det(random(size))
    return time.time() - a

def est(n):
    """Estimates the time taken to calculate a determinant
a size nxn  integer matrix using the triangular method.""" 
    
    a = 479/8578080
    b = -79/11040
    c = 1365449/4289040
    d = -15719/3404
    
    return a * n ** 3 + b * n ** 2 + c * n + d
