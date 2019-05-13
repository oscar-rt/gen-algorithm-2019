from ga_setup import settings
import random

#get random integer
def g_ri():
    return random.randint(0, settings["MAX_NUMBER"])

#get random operator
def g_ro():
    return random.choice(['+', '-', '*', '/'])

#percentage to result 0.0 - 1.0, returns true or false
def p_tr(percent):
    t_percent = percent * 100
    result = random.randint(0, 100)
    if result <= t_percent:
        return True
    else:
        return False 

cell_pool = []
#the cell class
class Cell:
    #default init constructor
    def __init__(self): 
        self.sequence = [g_ri(), g_ro(), g_ri(), g_ro(), g_ri(), g_ro(), g_ri()] #generate a random sequence of numbers and operators
        self.number = eval(''.join(str(e) for e in self.sequence)) #join sequence into string and evaluate the expression 
        self.emargin = abs(settings["TARGET_NUMBER"] - self.number) #error margin of the evaluated sequence
    #generate a cell from two other cells
    @classmethod
    def from_reproduction(self, cell_parent_1, cell_parent_2):
        #check if we're making a unique cell or not
        if settings["GENE_MONITORING"] == "ON":
            print("ON")#add functionality
        else: 
            #declare the sequence
            self.sequence = []
            #for every object in the sequence, choose which parent to inherit from at random
            for strand in range(7):
                parent_rand = random.choice([cell_parent_1, cell_parent_2])
                self.sequence.append(parent_rand.sequence[strand])
            #same as randomly generating a cell
            self.number = eval(''.join(str(e) for e in self.sequence)) #join sequence into string and evaluate the expression 
            self.emargin = abs(settings["TARGET_NUMBER"] - self.number) #error margin of the evaluated sequence
            #return a pointer to the object
            return self
cell = Cell()
cell2 = Cell()
cell3 = Cell.from_reproduction(cell, cell2)

cells = [cell, cell2, cell3]

for _cell in cells:
    print(_cell.sequence, _cell.number, _cell.emargin)
