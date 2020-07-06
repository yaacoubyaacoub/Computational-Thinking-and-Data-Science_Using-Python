###########################
# 6.0002 Problem Set 1a: Space Cows
# Name: Yaacoub Yaacoub
# Time:

from PS1_Partition import get_partitions
import time


# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    file = open(filename, "r")
    cows = {}
    for line in file.readlines():
        file_list = (line.rstrip()).split(",")
        cows[file_list[0]] = int(file_list[1])
    return cows


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    sorted_cows = {}
    for cow in sorted(cows.items(), key=lambda weight: weight[1], reverse=True):
        sorted_cows[cow[0]] = cow[1]
    cows_division = []
    while len(sorted_cows) > 0:
        the_limit = limit
        choosing_cows = []
        for cow in sorted_cows.keys():
            if sorted_cows[cow] <= the_limit:
                choosing_cows.append(cow)
                the_limit = the_limit - sorted_cows[cow]
        for cow in choosing_cows:
            del (sorted_cows[cow])
        cows_division.append(choosing_cows)
    return cows_division


# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    possible_distributions = []
    for a_distribution in get_partitions(cows):
        possible_distributions.append(a_distribution)
    possible_distributions.sort(key=len, reverse=True)
    flag = False
    the_optimal_distribution = []
    for distribution in possible_distributions:
        for dist in distribution:
            total_weight = 0
            for cow in dist:
                total_weight += cows[cow]
            if total_weight > limit:
                flag = False
                break
            else:
                flag = True
        if flag:
            if the_optimal_distribution == []:
                the_optimal_distribution = distribution
            elif len(distribution) <= len(the_optimal_distribution):
                the_optimal_distribution = distribution

    return the_optimal_distribution


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    cow_data = 1
    for file in ["PS1_Cow_Data.txt", "PS1_Cow_Data_2.txt"]:
        print("Cow Data ", str(cow_data) + ":")
        cow_data += 1
        greedy_start_time = time.time()
        greedy_cow_transp = greedy_cow_transport(load_cows(file), limit=10)
        greedy_stop_time = time.time()
        greedy_number_of_trips = len(greedy_cow_transp)
        greedy_runtime = float(greedy_stop_time - greedy_start_time)

        brute_force_start_time = time.time()
        brute_force_cow_trans = brute_force_cow_transport(load_cows(file), limit=10)
        brute_force_stop_time = time.time()
        brute_force_number_of_trips = len(brute_force_cow_trans)
        brute_force_runtime = float(brute_force_stop_time - brute_force_start_time)

        print("Greedy Cow Transport method:\n   - Number of trips:", greedy_number_of_trips, "\n   - runtime =",
              greedy_runtime, "s\n")
        print("Brute Force Cow Transport method:\n   - Number of trips:", brute_force_number_of_trips,
              "\n   - runtime =", brute_force_runtime, "s\n")
        print("---------------------------------")


compare_cow_transport_algorithms()
