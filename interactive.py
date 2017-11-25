from chemistry import *

def interactive():
    print(' '*12+'Chemistry\n\n**To exit at any time, press ctrl+c.\n')
    opt = input(
    """Pick one of the following:

A)General Facts
B)Find the Molar Mass of a Compound or Element
C)Convert Mass to Moles
D)Convert Moles to Mass
E)Balance a Chemical Equation\n\n"""
    )
    
    print('')
    
    if opt.lower() == 'a': 
        element  = input('Give the name, symbol, or atomic number of the element: ').lower().capitalize()
        category = input('\nOf the following list, which would you like to know:\n'+'~' * 80 +', '.join(categories)+'\n'+'~'*80+'\n')
        print()
        print(facts(element, category))
    
    elif opt.lower() == 'b':
        compound = input('What is the compound? ')
        print(mass(compound), 'g.')
    
    elif opt.lower() == 'c':
        compound  = input('\n~~Note: this tool negates stoichiometric coefficients.\n\nWhat is the compound? ')
        givenmass = input('What is the given mass in grams (only type the number): ')
        print(masstomoles(givenmass, compound), 'mol.')
    
    elif opt.lower() == 'd':
        compound = input('\n~~Note: this tool negates stoichiometric coefficients.\n\nWhat is the compound? ')
        moles    = input('What is the given number of moles (only type the number): ')
        print(molestomass(moles,compound),'g.')
    
    elif opt.lower() == 'e':
        reactants=input(
        """
~~Note: this tool is in its alpha-testing stage. It still has certain bugs.

What are the reactants of the equation? """
        )
        products=input('What the products of the equation?      ')
        
        try:
            print(addcoef(reactants, products, arrow = 1, showones = 0))
        
        except ValueError:
            print('--Calculation Failed--')
        
        except ZeroDivisionError:
            print('--Calculation Failed--')
    
    print()
     
interactive()
     
while input('Continue? (y/n) ').lower() in ['y', 'yes']:
    print()
    interactive()
