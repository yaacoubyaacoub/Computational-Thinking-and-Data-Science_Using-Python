###########################
# 6.0002 Problem Set 1b: Space Change
# Name: Yaacoub Yaacoub
# Time:
# Author: charz, cdenise

# ================================
# Part B: Golden Eggs
# ================================


# Problem 1
def dp_make_weight(egg_weights, target_weight, memo={}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """
    weight_index = []
    for j in range(1, len(egg_weights) + 1):
        weight_index.append(j)
    i = 1
    eggs_of_weight_i = 0
    for j in range(len(weight_index)):
        memo[egg_weights[len(egg_weights) - weight_index[j]]] = eggs_of_weight_i

    number_of_eggs = target_weight // egg_weights[len(egg_weights) - weight_index[0]]
    memo[egg_weights[len(egg_weights) - weight_index[0]]] = number_of_eggs
    target_weight = target_weight - number_of_eggs * egg_weights[len(egg_weights) - weight_index[0]]

    while target_weight != 0:
        if (target_weight - egg_weights[len(egg_weights) - weight_index[i]]) >= 0:
            target_weight = target_weight - egg_weights[len(egg_weights) - weight_index[i]]
            number_of_eggs += 1
            eggs_of_weight_i += 1
        else:
            memo[egg_weights[len(egg_weights) - weight_index[i]]] = eggs_of_weight_i
            eggs_of_weight_i = 0
            i += 1
        if target_weight == 0:
            memo[egg_weights[len(egg_weights) - weight_index[i]]] = eggs_of_weight_i
    return (number_of_eggs, memo)


# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n =", n)
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
