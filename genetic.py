import random
import matplotlib.pyplot as plt
import sys


def score(candidate):
    """
    The score of a candidate is the value of the items in the pack, unless the weight exceeds
    tolerance in which case the score is automatically zero.
    """
    score = sum([candidate[i]*items[i][0] for i in range(options)])
    weight = sum([candidate[i]*items[i][1] for i in range(options)])
    return 0 if weight > weightLimit else score


def cand():
    """
    Returns a candidate. A candidate is a list of zeros and ones of length <options>, where a one
    indicates that that option was selected for inclusion and a zero indicates it was not.
    """
    # return list(int(char) for char in f"{random.randint(0, 1<<options):b}".zfill(options))
    return [1 if random.random() > 0.5 else 0 for _ in range(options)]


def fight(cand1, cand2):
    """
    Fights two candidates against each other. The candidate with the higher score is returned
    as the winner. If their scores are equal, a random candidate is returned.
    """
    if score(cand1) > score(cand2):
        return cand1
    elif score(cand2) > score(cand1):
        return cand2
    else:
        return cand1 if random.random() > 0.5 else cand2


def next_parents(candidates):
    """
    Selects a new generation of parents by holding tournaments between the current generation.
    Two random candidates are selected. The candidate with the higher score is added to the new generation.
    Repeat random tournaments until the new generation is full.
    """
    ## Generate next generation parents.
    parents = list()
    while len(parents) < len(candidates):
        potential = fight(
                candidates[random.randint(0, members-1)],
                candidates[random.randint(0, members-1)]
            )
        if score(potential) > 0:
            parents.append(potential)
    return parents


def breed(cand1, cand2):
    """
    Breed two candidates by mixing their properties.
    """
    return cand1[:options//2] + cand2[options//2:]


def next_children(parents):
    """
    Create a new generation of children from a generation of parents.
    Parents are randomly paired and bred until the new generation of children is full.
    """
    children = list()
    while len(children) < len(parents):
        children.append(breed(parents[random.randint(0, members-1)], parents[random.randint(0, members-1)]))
    return children


def best(candidates):
    """
    Return the highest score from a selection of candidates.
    """
    return max([score(cand) for cand in candidates])


def mutate(candidate):
    """
    Randomly mutate a candidate. For each bit in the candidate, randomly flip the bit depending on mutation rate.
    Mutation rates too low will likely result in lack of diversity and little or no improvement over generations.
    Mutation rates too high will produce too much noise and generations may be either worse or better than the 
    previous generation.
    """
    for i in range(len(candidate)):
        mutation = random.random()
        if mutation < mutation_rate:
            candidate[i] = 1 if candidate[i] == 0 else 0
    return candidate


def generate_candidates(quantity=200):
    """
    Generate a quantity of candidates for the zeroth generation.
    """
    candidates = list()
    while len(candidates) < quantity:
        candidate = cand()
        if len(candidate) == options:
            candidates.append(candidate)
    passed = [1 for candidate in candidates if score(candidate) > 0]
    if sum(passed) < 2:
        print("First gen failure")
        return None
    return candidates


def variation(candidates):
    """
    Assesses the level of genetic variability in a generation.
    """
    giant = [sum([cand[i] for cand in candidates])-members//4 for i in range(options)]
    character = sum(giant)
    print(character, ": ", giant)
    return character


options = 16
members = 200
mutation_rate = 0.05
weightLimit = 20
generations = 200

print("Generating options")
#items = [[random.randint(0, 10), random.randint(1, 10)] for _ in range(options)]
items = [[9, 10], [2, 9], [0, 6], [0, 3], [6, 8], [1, 6], [5, 4], [7, 5], [8, 10], [9, 8], [6, 6], [7, 7], [9, 2], [1, 7], [1, 9], [5, 3]]
print("Generating first generation children")
children = generate_candidates(quantity=members)
if children is None:
    sys.exit(1)

variance = list()
scores = list()
for i in range(generations):
    # print(f"Computing generation {i+1} parents")
    parents = next_parents(children)
    # print(f"Computing generation {i+1} children")
    children = next_children(parents)
    # print(f"Mutating generation {i+1} children")
    mutated_children = [mutate(child) for child in children]
    scores.append(best(mutated_children))
    variance.append(variation(mutated_children))
    # print(f"Generation {i} best: {best(mutated_children)}")

for ech in mutated_children:
    print(ech)

plt.plot(scores)
plt.plot(variance)
plt.show()
