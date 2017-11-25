from tkinter import *
from .chemistry import *

win = Tk()
win.title('Chemistry')

f1 = Frame(win)
f = Frame(f1)
l = Label(f1, text = 'Chemistry\nChoose one of the following categories:')

b1 = Button(f, text = 'General Facts',command =  lambda: gen())
b2 = Button(f, text = 'Molar Mass',command = lambda: mm())
b3 = Button(f, text = 'Mass to Moles',command = lambda: ma2mo())
b4 = Button(f, text = 'Moles to Mass',command = lambda: mo2ma())
b5 = Button(f, text = 'Balance Chemical Equation',command = lambda: bchem())

b1.grid(row = 0, column = 0, padx = 3, pady = 3)
b2.grid(row = 1, column = 0, padx = 3, pady = 3)
b3.grid(row = 0, column = 1, padx = 3, pady = 3)
b4.grid(row = 1, column = 1, padx = 3, pady = 3)
b5.grid(row = 2, column = 0, columnspan = 2, padx = 3, pady = 3)

l.grid(pady = 3)
f.grid()
f1.grid()

f2 = Frame(win)
f2sub = Frame(f2)

def clearstr(svarname, svarname2 = 0):
    output = svarname.get()
    svarname.set('')
    if svarname2 != 0:
        output = [output,svarname2.get()]
        svarname2.set('')
    return output

def gen():
    f1.destroy()
    l = Label(f2, text = 'General Facts:\nType the name, atomic number, or atomic symbol of your element.')
    l2 = Label(f2sub)
    svar = StringVar()
    def command_a():
        global output
        output = clearstr(svar).title()
        if output in Num + Sym + Nam:    
            factspage()
        else:
            l2.configure(text = 'Invalid input, please try again.', fg = 'red')
    
    e  = Entry(f2sub,textvariable=svar,width=50)
    b1 = Button(f2sub,text='Enter',command = command_a)
    
    e.grid(sticky=W)
    b1.grid(sticky=W,pady=3)
    l2.grid()
    l.grid(pady=3)
    f2sub.grid()
    f2.grid()

def factspage():
    f3=Frame(win)
    f2.destroy()
    
    l  = Label(f3,text=facts(output,'name'))
    lb = Listbox(f3,height=10,width=50,bg='white')
    sb = Scrollbar(f3,orient=VERTICAL,command=lb.yview)
    lb.configure(yscrollcommand=sb.set)
    
    for n in categories:
        lb.insert(END,n.title()+': '+facts(output,n).title())
    
    l.grid(row=0,pady=3)
    lb.grid(row=1,column=0)
    sb.grid(row=1,column=1,rowspan=5)
    f3.grid()

def mm():
    f1.destroy()
    l = Label(f2, text = 'Molar Mass:\nType in the compound that you want the molar mass of.')
    l2 = Label(f2sub)
    svar = StringVar()
    def c1():
        output = clearstr(svar)
        if isvalid(output):
            l2.configure(text = 'The mass of {} is {} grams.'.format(output, round(mass(output), 4), fg = 'black'))
        else:
            l2.configure(text = 'Sorry, "{}" is not a valid element.\nPlease try again.'.format(isvalid(output, 1)), fg = 'red')
    e = Entry(f2sub, textvariable =  svar, width = 30)
    b1 = Button(f2sub, text = 'Enter', command = c1)
    l.grid()
    e.grid(sticky = W)
    b1.grid(sticky = W, pady = 3)
    l2.grid()
    f2sub.grid()
    f2.grid()

def ma2mo():
    f1.destroy()
    l = Label(f2, text = 'Mass to Moles\nType in the compound and the mass in grams that you have.')
    l2 = Label(f2, text = '**Note: This feature ignores stoichiometric coefficiants**', fg = 'blue')
    l3 = Label(f2sub, text = 'Compound:')
    l4 = Label(f2sub, text = 'Mass (grams):')
    l5 = Label(f2sub)
    svar1 = StringVar()
    svar2 = StringVar()
    def c1():
        outputs=clearstr(svar1,svar2)
        if isvalid(outputs[0]) and isnum(outputs[1]):
            l5.configure(text='{} grams of {} is equivalent to {} moles of {}.'.format(
            outputs[1], outputs[0], round(masstomoles(outputs[1], outputs[0]), outputs[0]), 4),fg='black')
        elif not isvalid(outputs[0]):
            l5.configure(text='Sorry, "{}" is not a valid element.\nPlease try again.'.format(isvalid(outputs[0],1)), fg='red')
        elif not isnum(outputs[1]):
            l5.configure(text='Sorry, your mass input is invalid,\nPlease try again.',fg='red')
    e1=Entry(f2sub,textvariable=svar1,width=30)
    e2=Entry(f2sub,textvariable=svar2,width=30)
    b1=Button(f2sub,text='Enter',command=c1)
    l.grid(pady=3)
    l2.grid()
    l3.grid(row=0,column=0)
    l4.grid(row=1,column=0)
    e1.grid(row=0,column=1)
    e2.grid(row=1,column=1)
    b1.grid(column=1)
    l5.grid(columnspan=2)
    f2sub.grid()
    f2.grid()

def mo2ma():
    f1.destroy()
    l=Label(f2,text='Moles to Mass\nType in the compound and the mass in grams that you have.')
    l2=Label(f2,text='**Note: This feature ignores stoichiometric coefficiants**', fg='blue')
    l3=Label(f2sub,text='Compound:')
    l4=Label(f2sub,text='Moles:')
    l5=Label(f2sub)
    svar1=StringVar()
    svar2=StringVar()
    def c1():
        outputs=clearstr(svar1,svar2)
        if isvalid(outputs[0]) and isnum(outputs[1]):
            l5.configure(text='{} moles of {} is equivalent to {} grams.'.format(
            outputs[1], outputs[0], round(molestomass(outputs[1],outputs[0]),outputs[0]), 4), fg='black')
        elif not isvalid(outputs[0]):
            l5.configure(text='Sorry, "{}" is not a valid element.\nPlease try again.'.format(isvalid(outputs[0],1)), fg='red')
        elif not isnum(outputs[1]):
            l5.configure(text='Sorry, your moles input is invalid,\nPlease try again.', fg='red')
    e1=Entry(f2sub,textvariable=svar1,width=30)
    e2=Entry(f2sub,textvariable=svar2,width=30)
    b1=Button(f2sub,text='Enter',command=c1)
    l.grid(pady=3)
    l2.grid()
    l3.grid(row=0,column=0)
    l4.grid(row=1,column=0)
    e1.grid(row=0,column=1)
    e2.grid(row=1,column=1)
    b1.grid(column=1)
    l5.grid(columnspan=2)
    f2sub.grid()
    f2.grid()

def bchem():
    f1.destroy()
    l=Label(f2,text="Chemical Equation Balancer\nType in the reactants and products of your equation.")
    l2=Label(f2,text='**Note: This feature ignores initial stoichiometric coefficiants**', fg='blue')
    l3=Label(f2sub,text='Reactants:')
    l4=Label(f2sub,text='Products:')
    l5=Label(f2sub)
    svar1=StringVar()
    svar2=StringVar()
    def c1():
        outputs=clearstr(svar1,svar2)
        outputsc=c2(outputs[0])+c2(outputs[1])
        k=1
        for n in outputsc:
            if not isvalid(n):
                l5.configure(text='Sorry, "{}" is not a valid element.\nPlease try again.', fg='red')
                k=0
                break
        if k:
            try:
                isbalanced(outputs[0],outputs[1])
            except ValueError:
                l5.configure(text='Sorry, your equation is invalid:\nYou have an element on one side of the\nequation that is not present on the other side.\nPlease try again.',fg='red')
                k=0
        if k:
            l5.configure(text='Balanced Equation: {}'.format(addcoef(outputs[0],outputs[1],arrow=1,showones=0)), fg='black')
    e1=Entry(f2sub,textvariable=svar1,width=30)
    e2=Entry(f2sub,textvariable=svar2,width=30)
    b1=Button(f2sub,text='Enter',command=c1)
    l.grid(pady=3)
    l2.grid()
    l3.grid(row=0,column=0)
    l4.grid(row=1,column=0)
    e1.grid(row=0,column=1)
    e2.grid(row=1,column=1)
    b1.grid(column=1)
    l5.grid(columnspan=2)
    f2sub.grid()
    f2.grid()

mainloop()
