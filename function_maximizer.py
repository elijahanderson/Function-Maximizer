"""
    AI PROJECT 3 by Eli Anderson

    This project involves writing a genetic algorithm to find the maximum value of arbitrary functions.

    The functions will be represented in text files, which begin with a line with a single number, representing the
    number of variables in the function. Each variable is an integer with a value ranging from 0 to 255.

    Click this link to see the rest of the project explanation: https://i.gyazo.com/1a4b33ca025f5f0a6d1286a647c140ff.png

    (Thede -- if you uncomment some of the lines of code, you can see how the program works step by step!)
"""

import operator
import random
import time
"""
    to calculate the values of each individual -- returns a dictionary containing the value of each indivdual's
                                                  variables run through the equation
"""
def calculate_values(pop, contents) :
    sum_dict = {}
    #print(contents)
    for key, value in pop.items() :
        # separate individuals into their variables, convert to decimal, store them in a dictionary
        var_dict = {}
        for i in range(num_vars) :
            pos = i * len(value) // num_vars
            var_dict[i] = int(value[pos:pos + 8], 2)
        #print('Individual ' + str(key) + ': ' + str(var_dict))
        # read from the text file to compute the sum of each individual
        sum = 0
        for row, line in enumerate(contents) :
            var = 0
            eles = line.split(' ')
            #print(eles)
            for col, coeff in enumerate(eles) :
                # skip over coeffs that have already been counted
                if row > col:
                    if col != 0:
                        var += 1
                    continue
                #print('Row: ' + str(row) + ' Column: ' + str(col) + ', ' + coeff + ', ' + str(var))
                # first coeff is never multiplied by anything
                if row == 0 and col == 0:
                    sum += int(coeff)
                # rest of first row is the coeff multiplied by just one appropriate variable
                elif row == 0 and col > 0:
                    sum += int(coeff) * var_dict[var]
                    var += 1
                # all other coeffs
                elif col > 0:
                    sum += int(coeff) * var_dict[row-1] * var_dict[var]
                    var += 1

        #print('Sum of individual ' + str(key) + ': ' + str(sum))
        #time.sleep(10)
        sum_dict[key] = sum
    return sum_dict
"""
    to evaluate the fitness of each population -- retuns a tuple where the first element is the new population and the
                                                  second is the best individual in the population
"""
def evaluate(pop) :
    print('=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print(pop)
    # evaluate the individual
    sum_dict = calculate_values(pop, contents6)
    print('The sums: ' + str(sum_dict))

    # to return later -- the expression returns the key of the largest value in sum_dict
    best = pop[max(sum_dict.items(), key=operator.itemgetter(1))[0]]

    # using the sum_dict, choose which the best individuals are passed into the next generation
    #print(pop)
    new_pop = {}
    A = max(sum_dict.items(), key=operator.itemgetter(1))[0]
    new_pop[0] = pop[A]
    # remove largest, find next largest
    sum_dict.pop(A)
    B = max(sum_dict.items(), key=operator.itemgetter(1))[0]
    new_pop[1] = pop[B]
    C = max(sum_dict.items(), key=operator.itemgetter(1))[0]
    new_pop[2] = pop[C]
    D = max(sum_dict.items(), key=operator.itemgetter(1))[0]
    new_pop[3] = pop[D]
    E = max(sum_dict.items(), key=operator.itemgetter(1))[0]
    new_pop[4] = pop[E]
    # we have a new population with the max two individuals of the old population
    #print(new_pop)
    # time to perform cross-over... select two points randomly within the bit string
    cross_pop = {}
    x = random.randint(0, len(new_pop[0]))
    y = random.randint(0, len(new_pop[0]))
    start = min(x, y)
    end = max(x, y)
    #print('Slicing from ' + str(start) + ' to ' + str(end))

    # each individual may get a portion of one of the two top individuals
    # the top individuals may remain the same, but that's fine
    for i in range(num_individuals) :
        j = random.randint(0, 4)
        # swap from top individuals
        cross_pop[i] = pop[i][:start]+new_pop[j][start:end]+pop[i][end:]

    # now for some fun -- it's time for mutation!
    #print('Before mutation: ' + str(cross_pop))
    mut_pop = {}
    for idv, value in cross_pop.items() :
        mut_pop[idv] = ''
        for i in range(len(value)) :
            if len(mut_pop[idv]) == bit_length:
                break
            # every bit will have a small chance of being flipped -- various testing has convinced me that a 1/150 chance is optimal
            else :
                mut_chance = random.randint(0, 150)
                if mut_chance == 0:
                    if cross_pop[idv][i] == '0':
                        mut_pop[idv] += '1'
                    else:
                        mut_pop[idv] += '0'
                    mut_pop[idv] += cross_pop[idv][i]
                else:
                    mut_pop[idv] += cross_pop[idv][i]
    #print('After mutation:  ' + str(mut_pop))
    return mut_pop, best

########################################################################################################################
# MAIN #################################################################################################################
########################################################################################################################

print('Welcome to Eli\'s function maximizer! Please enter the text file you want read: ', end='')
filename = input().strip()
generations = 1750
num_individuals = 1000

try :
    with open(filename, 'r') as file:
        # retrieve file contents, set each line as an element in a list
        contents = file.readlines()
        contents2 = contents[2:]
        # strip extra spaces, replace with spaces
        contents3 = [line.replace('    ', ' ') for line in contents2]
        contents4 = [line.replace('   ', ' ') for line in contents3]
        contents5 = [line.replace('  ', ' ') for line in contents4]
        # strip newlines
        contents6 = [line.strip() for line in contents5]
        print(contents6)
        #time.sleep(10)
        # get the number of variables
        num_vars = int(contents[0])
        print(num_vars)
        pop = {}

        # initialize the population -- the more individuals there are, the longer the algorithm will take
        for i in range(num_individuals) :
            pop[i] = ''

        # fill each individual with the appropriate number of random bits
        for key in pop:
            for i in range(num_vars) :
                pop[key] += str(random.randint(0, 1)) + str(random.randint(0, 1)) + str(random.randint(0, 1)) + str(random.randint(0, 1)) + \
                            str(random.randint(0, 1)) + str(random.randint(0, 1)) + str(random.randint(0, 1)) + str(random.randint(0, 1))
            print(pop[key])

        # get length of each bit string, this will be used later
        bit_length = len(pop[0])

        # put all the best individuals from each iteration into this dictionary:
        best_pop = {}

        # run the algorithm
        for i in range(generations) :
            pop, best = evaluate(pop)
            best_pop[i] = best
            print('The new population: ' + str(pop))
            print('The best performing individual: ' + best)
            # uncomment for periodic updates
            #time.sleep(1)

        print('=======================================================================================================')

        print('The best individual from every generation: ' + str(best_pop))

        # calculate the sums of the best individual from each generation
        best_sums = calculate_values(best_pop, contents6)
        # get the overall best indidvidual
        best_idv = best_pop[max(best_sums.items(), key=operator.itemgetter(1))[0]]

        # using the best binary number, print the best set of variables found
        best_dict = {}
        for i in range(num_vars):
            pos = i * len(best_idv) // num_vars
            best_dict[i] = int(best_idv[pos:pos + 8], 2)
        print('The best variables -- imagine there\'s an x in front of each number key: ' + str(best_dict))

        # print the value of the function with those variables
        sum = 0
        for row, line in enumerate(contents6) :
            var = 0
            eles = line.split(' ')
            #print(eles)
            for col, coeff in enumerate(eles) :
                # skip over coeffs that have already been counted
                if row > col:
                    if col != 0:
                        var += 1
                    continue
                #print('Row: ' + str(row) + ' Column: ' + str(col) + ', ' + coeff + ', ' + str(var))
                # first coeff is never multiplied by anything
                if row == 0 and col == 0:
                    sum += int(coeff)
                # rest of first row is the coeff multiplied by just one appropriate variable
                elif row == 0 and col > 0:
                    sum += int(coeff) * best_dict[var]
                    var += 1
                # all other coeffs
                elif col > 0:
                    sum += int(coeff) * best_dict[row-1] * best_dict[var]
                    var += 1

        print('Value of the function with those variables: ' + str(sum))

except FileNotFoundError :
    print('No file of that name detected; program terminated.')
