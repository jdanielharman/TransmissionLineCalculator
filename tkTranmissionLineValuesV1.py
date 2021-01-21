import tkinter as tk
import math

epsilon   = '\u03B5_r (Material Coefficent)'
sigma     = '\u03c3'
sigmaSubC = '\u03c3_c'
mu        = '\u03bc'
muSubC    = '\u03bc_c'
height    = 'b / D / h (Meters)'
width     = 'a / d / w (Meters)'
freq      = 'Frequency (Hz)'

coax     = 1
twoWire  = 2
parPlate = 3

fields = (freq,
          height,
          width,
          epsilon,
          sigma,
          sigmaSubC)

evalDic = {'pow' : math.pow, '^' : '**', 'E' : '*10**'}

def getResult(entries):
    e  = (float(eval(entries[epsilon].get(),    evalDic)))
    e *= 8.85 * math.pow(10, -12)
    s  = (float(eval(entries[sigma].get(),      evalDic)))
    sc = (float(eval(entries[sigmaSubC].get(),  evalDic)))
    u  = 12.57 * math.pow(10,-7)
    h  = (float(eval(entries[height].get(),     evalDic)))
    w  = (float(eval(entries[width].get(),      evalDic)))
    f  = (float(eval(entries[freq].get(),       evalDic)))
    select = int(selector.get())

    try:
        RS = math.sqrt(math.pi * f * (u / sc))
        if (select == coax):
            R = ( RS / (2*math.pi) ) * ( (1/h) + (1/w) )
            L = ( u  / (2*math.pi) ) * ( math.log(h/w) )
            G = ( 2 * math.pi * s  ) / ( math.log(h/w) )
            C = ( 2 * math.pi * e  ) / ( math.log(h/w) ) 
        elif (select == twoWire):
            x = math.log( (h/w) + math.sqrt( math.power((h/w), 2) - 1) )
            R = ( 2 * RS ) / ( math.pi * w )
            L = ( u / math.pi ) * x 
            G = ( math.pi * s ) / x
            C = ( math.pi * e ) / x 
        elif (select == parPlate):
            R = ( 2 * RS) / w
            L = ( u * h ) / w
            G = ( s * w ) / h
            C = ( e * w ) / h
        result  = "R' : {} \u03A9/m\n".format(R)
        result += "L' : {} H/m\n".format(L)
        result += "G' : {} S/m\n".format(G)
        result += "C' : {} F/m\n".format(C)
        b1.configure(text = result)
        
    except Exception as e:
        b1.configure(text = "Error, input variables please\n" + str(e))
        print(e)

def clearEntries(entries):
    for field in fields:
        entries[field].delete(0, 'end')
        entries[field].insert(0, '0')

# MakeForm - Creates input fields in a loop, based on the previous stuff
def makeform(root, fields):
    entries = {}
    for field in fields:
        print(field)
        row = tk.Frame(root)
        lab = tk.Label(row, width=22, text=field+": ", anchor='w')
        ent = tk.Entry(row)
        ent.insert(0, "0")
        row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT, 
                 expand=tk.YES, 
                 fill=tk.X)
        entries[field] = ent
    return entries

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Transmission Line Calculator')
    # Title
    title = tk.Label(text="Tranmission-Line Parameter Calculator\n")
    title.pack(side=tk.TOP, padx=2, pady=2)
    # Selector Label
    subtitle = tk.Label(text="Coaxial\t\tTwo-Wire\tParallel-Plate")
    subtitle.pack(side=tk.TOP, padx=2, pady=2)
    # Selector Scale
    selector = tk.Scale(root, from_=1, to=3, orient=tk.HORIZONTAL)
    selector.pack(side=tk.TOP, padx=2, pady=2)
    # Example Input
    example = tk.Label(text='Example Input: 1*10^-9 or 1E-9 or 1*10**-9')
    example.pack(side=tk.TOP, padx=5, pady=5)
    # Dictionary of entry fields
    ents = makeform(root, fields)
    clearEntries(ents)
    # Result Text
    b1 = tk.Label(root, text='Input Variables for Results')
    b1.pack(side=tk.TOP, padx=5, pady=5)
    # Calculate Button - Calculate Values
    b4 = tk.Button(root, text='Enter', command=(lambda e=ents: getResult(e)))
    b4.pack(side=tk.RIGHT, padx=25, pady=25)
    # Exit Button - Destroys window 
    b3 = tk.Button(root, text='Quit', command=root.destroy)
    b3.pack(side=tk.LEFT, padx=25, pady=25)
    # Clear Button - Clear All Cells
    b5 = tk.Button(root, text='Clear', command=(lambda e=ents: clearEntries(e)))
    b5.pack(side=tk.BOTTOM, padx=25, pady=25)
    # Run Main Tkinter Loop
    root.mainloop()
