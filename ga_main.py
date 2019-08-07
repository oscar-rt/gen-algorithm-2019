from ga_setup import settings
import random
import operator

###
##NOTES
### 
### Currently using hard-coded distribution function for reproduction spots, could be made into a setting
### Need to implement mutations 
### Should implement graphical representation of some kind 
###
###!CURRENT: Trying to figure out how to distribute child spots among cell hierarchy 

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
    def from_reproduction(cls, cell_parent_1, cell_parent_2):
        #we naturally break from this loop if no zero division error occurs
        while True:
        #check if we're making a unique cell or not
            try:
                if settings["GENE_MONITORING"] == "ON":
                    print("ON")#add functionality
                else:
                    cls = Cell() 
                    #declare the sequence
                    cls.sequence = []
                    #for every object in the sequence, choose which parent to inherit from at random
                    for strand in range(7):
                        mutation_threshold = random.randint(1, 100)
                        if mutation_threshold <= settings["MUTATION_RATE"] * 100:
                            if strand % 2 == 0:
                                cls.sequence.append(g_ri())
                            else: 
                                cls.sequence.append(g_ro())
                        else:
                            parent_rand = random.choice([cell_parent_1, cell_parent_2])
                            cls.sequence.append(parent_rand.sequence[strand])
                    #same as randomly generating a cell
                    cls.number = eval(''.join(str(e) for e in cls.sequence)) #join sequence into string and evaluate the expression 
                    cls.emargin = abs(settings["TARGET_NUMBER"] - cls.number) #error margin of the evaluated sequence
                    #return a pointer to the object
                    return cls
            except ZeroDivisionError:
                continue
            break
    
    def __str__(self):
         return str(self.sequence) + " " + str(self.number) + " " + str(self.emargin)

#important variables for main loop
generations = 0
reached_target = False
deaths = int(settings["DEATH_RATE"] * settings["MAX_POPULATION"] if settings["DEATH_RATE"] * settings["MAX_POPULATION"] <= settings["MAX_POPULATION"] - 1 else settings["MAX_POPULATION"] - 1)
child_spots = int(settings["MAX_POPULATION"] -  deaths)
rep_dict = {}
#################################################
#inital setup                                   #
#################################################
#generate max number of cells, fill up cell pool
for ci in range(settings["MAX_POPULATION"]):
    cell_pool.append(Cell())

def update_rd():
    #get number of cells in cell pool
    cnum = len(cell_pool)
    #for current cell iterator and current cell !CURRENT
    for num, cell in enumerate(cell_pool):
        pass

#get dynamic fitness-based distribution array of all cells in the pool
def get_distribution_array():
    
    d_array = []

    #get all emargins from the cell pool and find biggest e_margin (which should be last one anyway)
    l_emargin = 0
    for cell in cell_pool:
        d_array.append(cell.emargin)
        if cell.emargin > l_emargin:
            l_emargin = cell.emargin
    
    #turn all emargins into fitness maxes and get the sum of the fitness maxes
    t_sum = 0
    for i, d in enumerate(d_array):
        d_array[i] = (d - l_emargin) * -1
        t_sum = t_sum + d_array[i]
    
    #normalize fitness maxes in proportion to child spots
    
    for i, d in enumerate(d_array):
        d_array[i] = (d / t_sum) * child_spots
        

    #move surplus (decimal numbers) to next value, essentially distributing the children
    surplus = 0
    for i, d in reversed(list(enumerate(d_array))):
        
        d_array[i] = d_array[i] + surplus
        lcopy = float(d_array[i])
        d_array[i] = int(d_array[i])

        surplus = lcopy - int(lcopy)

    return d_array

mcell = Cell()
print(mcell)
fcell = Cell()
print(fcell)
scell = Cell().from_reproduction(mcell, fcell)
print(scell)

#main loop
while generations <= settings["MAX_GENERATIONS"] or not reached_target:
    #sort the cell pool so that the tippy top is the fittest
    cell_pool.sort(key=operator.attrgetter('emargin'))
    
    #go through the survival step
    del cell_pool[-deaths:]

    #update the reproduction dictionary
    rep_dict.clear()
    update_rd()

    #repopulate up until the max cell count, figure out how to divide the child spots among the sorted cell pool
    distribution_array = get_distribution_array()

    #check if any cell has reached the target fitness, if so, stop evolution
    for cell in cell_pool:
        if cell.emargin == 0:
            reached_target == True

    #go into the next generation
    generations = generations + 1

print(cell_pool)