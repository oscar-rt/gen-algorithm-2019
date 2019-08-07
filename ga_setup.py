
#check if all settins are properly set up
def check_settings():
    pass

settings = {
    #the generation limit, grinds the program to a halt if not yet found
    "MAX_GENERATIONS" : 10000,
    #the maximum number of cells, anywhere from 1 to 17297280
    "MAX_POPULATION" : 100,
    #what percentage of the population dies 0-1
    "DEATH_RATE" : .5,
    #the rate at which a mutation can occur 0-1
    "MUTATION_RATE" : .01,
    #maximum integer generated, upper bound is inclusive, should be equal to or less than target
    "MAX_NUMBER" : 100,
    #the target integer
    "TARGET_NUMBER" : 45,
    #controls wether cell will check for duplicates before reproducing, only relevant in 
    #large children pools: ON or OFF 
    "GENE_MONITORING" : "OFF"
}

