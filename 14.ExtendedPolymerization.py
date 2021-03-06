import datetime
from blist import blist
import numpy as np
import collections

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test14.txt') as f:
    INPUT_TEST = f.read()

with open('input/input14.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    template, rules_raw = input.split('\n\n')
    rules = [row.split(' -> ') for row in rules_raw.split('\n')]
    return blist(list(template)), {tuple(r[0]): r[1] for r in rules} # Use blist instead of list for better performance on inserting to middle of list

def insert(polymer, rules, nsteps):
    for step in range(nsteps):
        i = 0
        while (i < len(polymer)-1):
            pair = tuple(polymer[i:i+2])
            inserted_element = rules[pair] if pair in rules else None
            if inserted_element is None:
                i+=1
                continue
            polymer.insert(i+1, inserted_element)
            i+=2 # Skip newly inserted element in this step
    return polymer

def part1(input):
    polymer, rules = input
    polymer = insert(polymer, rules, 10)
    frequency_counts = np.unique(np.array(polymer), return_counts=True)
    print(f"After 10 steps, polymer length is {len(polymer)}.")
    return np.max(frequency_counts[1]) - np.min(frequency_counts[1])

# Tracking whole polymer sequence like in part 1 takes way too long due to polymer length after steps 20+
# Approach: Supposed there is a rule AB -> C. At any step t, if polymer contains n pairs AB at any position, then in step t+1:
#          1. n pairs AB from previous step are decomissioned
#          2. n pairs AC & n pairs CB are created 
# Instead of tracking whole polymer sequence, we just need to keep track of frequency counts of element pairs in each step.
def part2(input):
    polymer, rules = input
    # Pre-populate all 2 pairs that generated by each single rule after 1 step
    # For example: {('C', 'H'): [('C', 'B'), ('B', 'H')], 
    #               ('H', 'H'): [('H', 'N'), ('N', 'H')],...}
    next_step_pairs = {}
    for rule_pair in [blist(k) for k in rules.keys()]:
        next_step_polymer = insert(rule_pair.copy(), rules, nsteps = 1)
        pair_counts = [tuple(next_step_polymer[i:i+2]) for i in range(len(next_step_polymer) - 1)]
        next_step_pairs[tuple(rule_pair)] = pair_counts
    
    # Starting from initial pairs in template, calculate number of pairs created after each step based on prepopulated rules above
    template_pairs = [tuple(polymer[i:i+2]) for i in range(len(polymer) - 1)]
    polymer_pair_counter = collections.Counter(template_pairs)
    for i in range(40):
        current_polymer_counter = collections.Counter([])
        for p in polymer_pair_counter:
            n_pairs = polymer_pair_counter[p]
            created_pairs = collections.Counter({k: n_pairs for k in next_step_pairs[p]})
            current_polymer_counter = current_polymer_counter + created_pairs
        polymer_pair_counter = current_polymer_counter

    # Derive frequency counts of elements final polymer from counts of pairs
    element_counter = collections.Counter({k:0 for k  in set([e for p in rules.keys() for e in p])})
    for p in polymer_pair_counter:
        for e in element_counter:
            if(e in p): element_counter[e] += polymer_pair_counter[p]
            if (p == (e,e)): element_counter[e] += polymer_pair_counter[p] # pairs of same elements such as ('H', 'H'): 100 are counted twice into final element count
    element_counter = {k:element_counter[k]//2 for k in element_counter}
    
    # First and last emelemts in the intial template polymer appear in only 1 pair each => add 1 to counts of these 2 elements
    element_counter[polymer[0]] += 1
    element_counter[polymer[-1]] += 1
    sorted_element_counter = {k: v for k, v in sorted(element_counter.items(), key=lambda item: item[1])}
    print(f"Number of elements after 40 steps from least to most common: {sorted_element_counter}")
    return max(element_counter.values()) - min (element_counter.values())

if __name__ == "__main__":
    if(exec_test_case == 0):
        inputs = [INPUT]
    else:
        inputs = INPUT_TEST.split("\n#####INPUT_SEPERATOR#####\n")
    
    if exec_test_case > len(inputs):
        print(f"Test case {exec_test_case} does not exist")
        quit()
    for i, input_str in enumerate(inputs):
        if(exec_test_case == 0):
            print(f"Running real puzzle input...")
        elif (exec_test_case == -1):
            print(f"Running test case {i+1}/{len(inputs)}...")
        else:
            if (i+1 == exec_test_case):
                print(f"Running test case {i+1}/{len(inputs)}...")
            else:
                continue
            
        input = parse_input(input_str)
        start_time = datetime.datetime.now() 
        if (exec_part == 1):
            result = part1(input)
        else:
            result = part2(input)
        end_time = datetime.datetime.now() 

        print('Part {} time: {}'.format(exec_part, end_time - start_time))
        print('Part {} answer: {}\n'.format(exec_part, result))

