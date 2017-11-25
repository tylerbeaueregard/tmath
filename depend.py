import importlib as ilib

if ilib.find_loader('sympy') == None:
    import pip
    pip.main(['install', 'sympy'])
if ilib.find_loader('matplotlib') == None:
    import pip
    pip.main(['install', 'matplotlib'])
