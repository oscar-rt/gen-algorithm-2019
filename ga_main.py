from ga_setup import settings
import random
import operator

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
        while True:
            try:
                self.sequence = [g_ri(), g_ro(), g_ri(), g_ro(), g_ri(), g_ro(), g_ri()] #generate a random sequence of numbers and operators
                self.number = eval(''.join(str(e) for e in self.sequence)) #join sequence into string and evaluate the expression 
                self.emargin = abs(settings["TARGET_NUMBER"] - self.number) #error margin of the evaluated sequence
            except ZeroDivisionError:
                continue
            break
    #generate a cell from two other cells
    @classmethod
    def from_reproduction(self, cell_parent_1, cell_parent_2):
        while True:
        #check if we're making a unique cell or not
            try:
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
            except ZeroDivisionError:
                continue
            break
    
    def __str__(self):
         return str(self.sequence) + " " + str(self.number) + " " + str(self.emargin)

#important variables for main loop
generations = 0
reached_target = False
deaths = settings["DEATH_RATE"] * settings["MAX_POPULATION"] if settings["DEATH_RATE"] * settings["MAX_POPULATION"] <= settings["MAX_POPULATION"] - 1 else settings["MAX_POPULATION"] - 1
child_spots = settings["MAX_POPULATION"] -  deaths
#################################################
#inital setup                                   #
#################################################
#generate max number of cells, fill up cell pool
for ci in range(settings["MAX_POPULATION"]):
    cell_pool.append(Cell())

#main loop
while generations <= settings["MAX_GENERATIONS"] or not reached_target:
    #sort the cell pool so that the tippy top is the fittest
    cell_pool.sort(key=operator.attrgetter('emargin'))
    
    #go through the survival step
    del cell_pool[-deaths:]

    #repopulate up until the max cell count, figure out how to divide the child spots among the sorted cell pool


    generations = generations + 1