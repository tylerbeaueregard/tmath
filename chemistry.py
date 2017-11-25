"""Chemistry Basics- Tyler Beauregard: These 
are used by "ChemistryGUI.py", but can also be 
used by themself for the more experienced user."""

import re
from matrix import *
from fractions import Fraction, gcd

def lcm(*args):
    if len(args) == 2:
        a, b = args[0], args[1]
        try:
            ans = Fraction(abs(a * b), gcd(a, b))
            if ans == int(ans):
                ans = int(ans)
            return ans
        except TypeError:
            return abs(a * b) / gcd(a, b)
    else:
        args = [lcm(args[0], args[1])] + list(args)[2:]
        return lcm(*args)

Elements = open('elements.txt')
categories = Elements.readline()[:-1].split(',')
stats = [line.split(',') for line in Elements.read().split('\n')] 
[Num, Sym, Nam] = [[row[collumn] for row in stats] for collumn in [0, 1, 2]]
Elements.close()


#The following functions help internally, shortening things up.
def indeces(Lis, element):
    ans, Lis = [], list(Lis)
    for n in range(len(Lis)):
        if Lis[n] == element:
            ans+=[n]
    return ans
def isnum(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
def splitnum(string, loc = 0, showones = 0):
    coef = ''
    if str(loc).lower() in ['end', '1', 'e']:
        string = string[::-1]
    for n in string:
        if n.isnumeric():
            coef += n
        else:
            break
    if str(loc).lower() in ['end', '1', 'e']:
        coef = coef[::-1]
    if showones and coef == '':
        coef += '1'
    return coef


#The following functions help to parse user input.
def c1(compound, showones = 0):
    sto_coef = splitnum(compound, 0, showones)
    compound = compound[len(splitnum(compound, 0)):]
    if compound[0].islower(): return 0
    compound = re.findall(r'[A-Z]{1}[a-z]*\d*', compound)
    if showones:
        for n in range(len(compound)):
            if not compound[n][-1].isnumeric():
                compound[n] += '1'
    return [sto_coef, compound]
def c2(summ):
    return summ.split('+')


#The following function returns a fact pertaining to a certain element.
def facts(element, category = 'atomic mass'):
    valdict={'mass':'atomic mass', 'molar mass':'atomic mass', 'electron configuration':'electronic configuration', 'number':'atomic number'}
    category, element = category.lower(), str(element).title()
    if category in valdict:
        category = valdict[category]
    if element in Nam:
        element = Nam.index(element) + 1
    elif element in Sym:
        element = Sym.index(element) + 1
    elif element not in Num:
        raise ValueError('The element or category is invalid.')
    try:
        return stats[int(element) - 1][indeces(categories, category)[0]]
    except IndexError:
        return 'N/A'


#The following functions varifiy and interperet user input.
def elemin(C, shownum = 0):
    if '+' in C:
        return [elemin(k, shownum) for k in C.split('+')]
    
    ans, num, fin_num = [], [], []
    C = c1(C, 1)[-1]
    
    for k in C:
        p = splitnum(k, 1)
        ans.append(k[:len(k) - len(p)])
        num.append(p)
    
    for n in set(ans):
        fin_num += [sum([int(num[h]) for h in indeces(ans,n)])]
    
    if shownum:
        return [list(set(ans)), fin_num]
    
    return list(set(ans))
def isvalid(C, show = 0):
    h = C[len(splitnum(C, 0)):]
    v = 1
    if h == '' or h[0].islower():
        return 0
    else:
        for k in elemin(C):
            if not k in Sym:
                v = 0
                h = [k]
                break
    if show and not v:
        return h[0]
    return v
def howmany(C,elem):
    try:
        k = dict()
        for n in elemin(C):
            k[n] = elemin(C, 1)[1][indeces(elemin(C),n)[0]]
        return k[elem]
    except KeyError:
        return 0


#The following functions deal with mass and mass-related operations.
def mass(compound):
    if '+' in compound:
        return sum([mass(part) for part in compound.split('+')])
    if type(compound) == str:
        compound = c1(compound, 1)
    ans = 0
    for n in compound[1]:
        num = splitnum(n, 1)
        part = n[:len(n) - len(num)]
        ans += float(facts(part)) * int(num)
    return int(compound[0]) * ans
def masstomoles(givenmass, compound):
    return float(givenmass) / mass(compound)
def molestomass(moles, compound):
    return float(moles) * mass(compound)


#The following finctions pertain to balancing chemical equations. It is still expiramental and has various bugs.
def isbalanced(R, P):
    R, P, s1, s2 = R.split('+'), P.split('+'), [], []
    for n in R + P:
        if not isvalid(n):
            raise ValueError('Your equation is invalid: "{}" is not a valid element.'.format(isvalid(n,1)))
    for n in R:
        s1 += elemin(n)
    for n in P:
        s2 += elemin(n)
    if set(s1) != set(s2):
        raise ValueError('Your equation is invalid: You have an element on one side of the equation that is not present on the other side.')
    R, P = '+'.join(R), '+'.join(P)
    return abs(mass(R) - mass(P)) <= 1e-4


def balance(R, P):
    
    if isbalanced(R,P):
        return [int(splitnum(n, 0, 1)) for n in c2(R) + c2(P)]
    
    ellist, ellist2, eqlist = [], [], []
    
    for k in elemin(R + '+' + P):
        ellist += k
    
    for n in ellist:
        if n not in ellist2:
            ellist2.append(n)
    
    for n in ellist2:
        coeflist=[]
        for k in R.split('+'):
            coeflist.append(howmany(k, n))
        for k in P.split('+'):
            coeflist.append(-howmany(k, n))
        eqlist.append(coeflist)
    
    eqlist2 = [-n[-1] for n in eqlist]
    eqlist  = [n[:-1] for n in eqlist]
    
    mat1 = Matrix(*eqlist)
    mat2 = Matrix(*[[n] for n in eqlist2])

    if not mat1.is_square():
        mat1 = Matrix(*mat1.rows[:len(mat1.columns)])
        mat2 = Matrix(*mat2.rows[:len(mat1.columns)])

    #print(mat1, mat2, sep = '\n\n')

    syst = mat1.cofactor(tri = 0).transpose() * mat2
    last = Fraction(mat1.determinant(tri = 0), 1)
    
    a = []
    
    for n in syst.rows:
        for k in n:
            a.append(k)
    
    a.append(last)

    #print(a)
    
    m = lcm(*[Fraction(1, n) for n in a])
    
    m = int(1/m)
    
    return [abs(int(n/m)) for n in a]
def addcoef(R, P, clist = None, arrow = 0, showones = 1):
    r, p = [n for n in R if n != ' '], [n for n in P if n != ' ']
    R, P = ''.join(r), ''.join(p)
    if clist == None:
        clist = balance(R,P)
        if showones == 0:
            for n in indeces(clist, 1):
                clist[n]=''
    Rn, Pn = '', ''
    for k in range(len(R.split('+'))):
        n = R.split('+')[k]
        Rn += str(clist[k]) + n[len(splitnum(n,0)):] + ' + '
    for k in range(len(c2(P))):
        n = c2(P)[k]
        Pn += str(clist[k + len(c2(R))]) + n[len(splitnum(n, 0)):] + ' + '
    Rn, Pn = Rn[:-3], Pn[:-3]
    if arrow == 1:
        return Rn + ' -> ' + Pn
    return Rn, Pn