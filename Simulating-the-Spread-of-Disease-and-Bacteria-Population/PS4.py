# Problem Set 4: Simulating the Spread of Disease and Bacteria Population Dynamics
# Name: Yaacoub Yaacoub
# Time:

import math
import numpy as np
import pylab as pl
import random


##########################
# End helper code
##########################

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleBacteria
    and ResistantBacteria classes to indicate that a bacteria cell does not
    reproduce. You should use NoChildException as is; you do not need to
    modify it or add any code.
    """


def make_one_curve_plot(x_coords, y_coords, x_label, y_label, title):
    """
    Makes a plot of the x coordinates and the y coordinates with the labels
    and title provided.

    Args:
        x_coords (list of floats): x coordinates to graph
        y_coords (list of floats): y coordinates to graph
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): title for the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords)
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


def make_two_curve_plot(x_coords, y_coords1, y_coords2, y_name1, y_name2, x_label, y_label, title):
    """
    Makes a plot with two curves on it, based on the x coordinates with each of
    the set of y coordinates provided.

    Args:
        x_coords (list of floats): the x coordinates to graph
        y_coords1 (list of floats): the first set of y coordinates to graph
        y_coords2 (list of floats): the second set of y-coordinates to graph
        y_name1 (str): name describing the first y-coordinates line
        y_name2 (str): name describing the second y-coordinates line
        x_label (str): label for the x-axis
        y_label (str): label for the y-axis
        title (str): the title of the graph
    """
    pl.figure()
    pl.plot(x_coords, y_coords1, label=y_name1)
    pl.plot(x_coords, y_coords2, label=y_name2)
    pl.legend()
    pl.xlabel(x_label)
    pl.ylabel(y_label)
    pl.title(title)
    pl.show()


##########################
# PROBLEM 1
##########################

class SimpleBacteria(object):
    """A simple bacteria cell with no antibiotic resistance"""

    def __init__(self, birth_prob, death_prob):
        """
        Args:
            birth_prob (float in [0, 1]): Maximum possible reproduction
                probability
            death_prob (float in [0, 1]): Maximum death probability
        """
        self.birth_probability = birth_prob
        self.death_probability = death_prob

    def is_killed(self):
        """
        Stochastically determines whether this bacteria cell is killed in
        the patient's body at a time step, i.e. the bacteria cell dies with
        some probability equal to the death probability each time step.

        Returns:
            bool: True with probability self.death_prob, False otherwise.
        """
        bacteria = random.choices(["killed", "not killed"],
                                  weights=[self.death_probability, 1 - self.death_probability])
        if bacteria == ["killed"]:
            return True
        else:
            return False

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes.

        The bacteria cell reproduces with probability
        self.birth_prob * (1 - pop_density).

        If this bacteria cell reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleBacteria (which has the same
        birth_prob and death_prob values as its parent).

        Args:
            pop_density (float): The population density, defined as the
                current bacteria population divided by the maximum population

        Returns:
            SimpleBacteria: A new instance representing the offspring of
                this bacteria cell (if the bacteria reproduces). The child
                should have the same birth_prob and death_prob values as
                this bacteria.

        Raises:
            NoChildException if this bacteria cell does not reproduce.
        """
        reproduce_probability = self.birth_probability * (1 - pop_density)
        reproduce = random.choices(["reproduce", "does not reproduce"],
                                   weights=[reproduce_probability, 1 - reproduce_probability])
        if reproduce == ["reproduce"]:
            return SimpleBacteria(self.birth_probability, self.death_probability)
        else:
            raise NoChildException("This bacteria cell does not reproduce")


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any
    antibiotics and his/her bacteria populations have no antibiotic resistance.
    """

    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria (list of SimpleBacteria): The bacteria in the population
            max_pop (int): Maximum possible bacteria population size for
                this patient
        """
        self.bacteria = bacteria
        self.max_pop = max_pop

    def get_total_pop(self):
        """
        Gets the size of the current total bacteria population.

        Returns:
            int: The total bacteria population
        """
        return len(self.bacteria)

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute the following steps in
        this order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. Calculate the current population density by dividing the surviving
           bacteria population by the maximum population. This population
           density value is used for the following steps until the next call
           to update()

        3. Based on the population density, determine whether each surviving
           bacteria cell should reproduce and add offspring bacteria cells to
           a list of bacteria in this patient. New offspring do not reproduce.

        4. Reassign the patient's bacteria list to be the list of surviving
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        surviving_bacteria = []
        for bacteria in self.bacteria:
            if not bacteria.is_killed():
                surviving_bacteria.append(bacteria)
        population_density = len(surviving_bacteria) / self.max_pop
        new_offspring = []
        for bacteria in surviving_bacteria:
            try:
                new_bacteria = bacteria.reproduce(population_density)
                new_offspring.append(new_bacteria)
            except:
                pass
        self.bacteria.clear()
        self.bacteria = surviving_bacteria + new_offspring
        return len(self.bacteria)


##########################
# PROBLEM 2
##########################

def calc_pop_avg(populations, n):
    """
    Finds the average bacteria population size across trials at time step n

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j

    Returns:
        float: The average bacteria population size at time step n
    """
    bacteria_population_sum = 0
    for i in range(0, len(populations)):
        bacteria_population_sum += populations[i][n]
    average_bacteria_population_in_n = bacteria_population_sum / (len(populations))
    return average_bacteria_population_in_n


def simulation_without_antibiotic(num_bacteria, max_pop, birth_prob, death_prob, num_trials):
    """
    Run the simulation and plot the graph for problem 2. No antibiotics
    are used, and bacteria do not have any antibiotic resistance.

    For each of num_trials trials:
        * instantiate a list of SimpleBacteria
        * instantiate a Patient using the list of SimpleBacteria
        * simulate changes to the bacteria population for 300 timesteps,
          recording the bacteria population after each time step. Note
          that the first time step should contain the starting number of
          bacteria in the patient

    Then, plot the average bacteria population size (y-axis) as a function of
    elapsed time steps (x-axis) You might find the make_one_curve_plot
    function useful.

    Args:
        num_bacteria (int): number of SimpleBacteria to create for patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float in [0, 1]): maximum reproduction
            probability
        death_prob (float in [0, 1]): maximum death probability
        num_trials (int): number of simulation runs to execute

    Returns:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria in trial i at time step j
    """
    bacteria = []
    for i in range(0, num_bacteria):
        bacteria.append(SimpleBacteria(birth_prob, death_prob))
    print("Loading .", end="")
    populations = []
    time_steps = 300
    for i in range(0, num_trials):
        patient = Patient(bacteria.copy(), max_pop)
        nb_of_bacteria = []
        for time_step in range(0, time_steps):
            if time_step == 0:
                nb_of_bacteria.append(patient.get_total_pop())
            else:
                nb_of_bacteria.append(patient.update())
        populations.append(nb_of_bacteria)
        print(".", end="")
    print(" Done")
    average_list = []
    x_coordinates = []
    for n in range(0, time_steps):
        x_coordinates.append(n)
        average_list.append(calc_pop_avg(populations, n))
    make_one_curve_plot(x_coordinates, average_list, "Timestep", "Average Population",
                        "Average Bacteria Populationper Timestep (Without Antibiotics)")
    return populations


# When you are ready to run the simulation, uncomment the next line
populations = simulation_without_antibiotic(100, 1000, 0.1, 0.025, 50)


##########################
# PROBLEM 3
##########################

def calc_pop_std(populations, t):
    """
    Finds the standard deviation of populations across different trials
    at time step t by:
        * calculating the average population at time step t
        * compute average squared distance of the data points from the average
          and take its square root

    You may not use third-party functions that calculate standard deviation,
    such as numpy.std. Other built-in or third-party functions that do not
    calculate standard deviation may be used.

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        float: the standard deviation of populations across different trials at
             a specific time step
    """
    average = calc_pop_avg(populations, t)
    average_square_distance = 0
    for i in range(0, len(populations)):
        average_square_distance += (populations[i][t] - average) ** 2
    standard_deviation = math.sqrt(average_square_distance / len(populations))
    return standard_deviation


def calc_95_ci(populations, t):
    """
    Finds a 95% confidence interval around the average bacteria population
    at time t by:
        * computing the mean and standard deviation of the sample
        * using the standard deviation of the sample to estimate the
          standard error of the mean (SEM)
        * using the SEM to construct confidence intervals around the
          sample mean

    Args:
        populations (list of lists or 2D array): populations[i][j] is the
            number of bacteria present in trial i at time step j
        t (int): time step

    Returns:
        mean (float): the sample mean
        width (float): 1.96 * SEM

        I.e., you should return a tuple containing (mean, width)
    """
    mean = calc_pop_avg(populations, t)
    SEM = calc_pop_std(populations, t) / math.sqrt(len(populations))
    width = 1.96 * SEM
    return mean, width


##########################
# PROBLEM 4
##########################

class ResistantBacteria(SimpleBacteria):
    """A bacteria cell that can have antibiotic resistance."""

    def __init__(self, birth_prob, death_prob, resistant, mut_prob):
        """
        Args:
            birth_prob (float in [0, 1]): reproduction probability
            death_prob (float in [0, 1]): death probability
            resistant (bool): whether this bacteria has antibiotic resistance
            mut_prob (float): mutation probability for this
                bacteria cell. This is the maximum probability of the
                offspring acquiring antibiotic resistance
        """
        SimpleBacteria.__init__(self, birth_prob, death_prob)
        self.resistant = resistant
        self.mut_prob = mut_prob

    def get_resistant(self):
        """Returns whether the bacteria has antibiotic resistance"""
        return self.resistant

    def is_killed(self):
        """Stochastically determines whether this bacteria cell is killed in
        the patient's body at a given time step.

        Checks whether the bacteria has antibiotic resistance. If resistant,
        the bacteria dies with the regular death probability. If not resistant,
        the bacteria dies with the regular death probability / 4.

        Returns:
            bool: True if the bacteria dies with the appropriate probability
                and False otherwise.
        """
        if self.resistant:
            bacteria = random.choices(["killed", "not killed"],
                                      weights=[self.death_probability, 1 - self.death_probability])
        elif not self.resistant:
            resistant_death_probability = self.death_probability / 4
            bacteria = random.choices(["killed", "not killed"],
                                      weights=[resistant_death_probability, 1 - resistant_death_probability])
        if bacteria == ["killed"]:
            return True
        else:
            return False

    def reproduce(self, pop_density):
        """
        Stochastically determines whether this bacteria cell reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A surviving bacteria cell will reproduce with probability:
        self.birth_prob * (1 - pop_density).

        If the bacteria cell reproduces, then reproduce() creates and returns
        an instance of the offspring ResistantBacteria, which will have the
        same birth_prob, death_prob, and mut_prob values as its parent.

        If the bacteria has antibiotic resistance, the offspring will also be
        resistant. If the bacteria does not have antibiotic resistance, its
        offspring have a probability of self.mut_prob * (1-pop_density) of
        developing that resistance trait. That is, bacteria in less densely
        populated environments have a greater chance of mutating to have
        antibiotic resistance.

        Args:
            pop_density (float): the population density

        Returns:
            ResistantBacteria: an instance representing the offspring of
            this bacteria cell (if the bacteria reproduces). The child should
            have the same birth_prob, death_prob values and mut_prob
            as this bacteria. Otherwise, raises a NoChildException if this
            bacteria cell does not reproduce.
        """
        reproduce_probability = self.birth_probability * (1 - pop_density)
        reproduce = random.choices(["reproduce", "does not reproduce"],
                                   weights=[reproduce_probability, 1 - reproduce_probability])
        if reproduce == ["reproduce"]:
            if self.resistant:
                return ResistantBacteria(self.birth_probability, self.death_probability, self.resistant, self.mut_prob)
            elif not self.resistant:
                mutation_probability = self.mut_prob * (1 - pop_density)
                is_resistant = random.choices([True, False], weights=[mutation_probability, 1 - mutation_probability])
                return ResistantBacteria(self.birth_probability, self.death_probability, is_resistant[0], self.mut_prob)
        else:
            raise NoChildException("This bacteria cell does not reproduce")


class TreatedPatient(Patient):
    """
    Representation of a treated patient. The patient is able to take an
    antibiotic and his/her bacteria population can acquire antibiotic
    resistance. The patient cannot go off an antibiotic once on it.
    """

    def __init__(self, bacteria, max_pop):
        """
        Args:
            bacteria: The list representing the bacteria population (a list of
                      bacteria instances)
            max_pop: The maximum bacteria population for this patient (int)

        This function should initialize self.on_antibiotic, which represents
        whether a patient has been given an antibiotic. Initially, the
        patient has not been given an antibiotic.

        Don't forget to call Patient's __init__ method at the start of this
        method.
        """
        Patient.__init__(self, bacteria, max_pop)
        self.on_antibiotic = False

    def set_on_antibiotic(self):
        """
        Administer an antibiotic to this patient. The antibiotic acts on the
        bacteria population for all subsequent time steps.
        """
        self.on_antibiotic = True

    def get_resist_pop(self):
        """
        Get the population size of bacteria cells with antibiotic resistance

        Returns:
            int: the number of bacteria with antibiotic resistance
        """
        number_of_resistant_bacteria = 0
        for b in self.bacteria:
            if b.get_resistant():
                number_of_resistant_bacteria += 1
        return number_of_resistant_bacteria

    def update(self):
        """
        Update the state of the bacteria population in this patient for a
        single time step. update() should execute these actions in order:

        1. Determine whether each bacteria cell dies (according to the
           is_killed method) and create a new list of surviving bacteria cells.

        2. If the patient is on antibiotics, the surviving bacteria cells from
           (1) only survive further if they are resistant. If the patient is
           not on the antibiotic, keep all surviving bacteria cells from (1)

        3. Calculate the current population density. This value is used until
           the next call to update(). Use the same calculation as in Patient

        4. Based on this value of population density, determine whether each
           surviving bacteria cell should reproduce and add offspring bacteria
           cells to the list of bacteria in this patient.

        5. Reassign the patient's bacteria list to be the list of survived
           bacteria and new offspring bacteria

        Returns:
            int: The total bacteria population at the end of the update
        """
        surviving_bacteria = []
        for bacteria in self.bacteria:
            if not bacteria.is_killed():
                surviving_bacteria.append(bacteria)

        surviving_bacteria_after_antibiotic = []
        if self.on_antibiotic:
            for bacteria in surviving_bacteria:
                if bacteria.get_resistant():
                    surviving_bacteria_after_antibiotic.append(bacteria)
        elif not self.on_antibiotic:
            surviving_bacteria_after_antibiotic = surviving_bacteria

        population_density = len(surviving_bacteria_after_antibiotic) / self.max_pop

        new_offspring = []
        for bacteria in surviving_bacteria_after_antibiotic:
            try:
                new_bacteria = bacteria.reproduce(population_density)
                new_offspring.append(new_bacteria)
            except:
                pass
        self.bacteria.clear()
        self.bacteria = surviving_bacteria_after_antibiotic + new_offspring
        return len(self.bacteria)


##########################
# PROBLEM 5
##########################

def simulation_with_antibiotic(num_bacteria, max_pop, birth_prob, death_prob, resistant, mut_prob, num_trials):
    """
    Runs simulations and plots graphs for problem 4.

    For each of num_trials trials:
        * instantiate a list of ResistantBacteria
        * instantiate a patient
        * run a simulation for 150 timesteps, add the antibiotic, and run the
          simulation for an additional 250 timesteps, recording the total
          bacteria population and the resistance bacteria population after
          each time step

    Plot the average bacteria population size for both the total bacteria
    population and the antibiotic-resistant bacteria population (y-axis) as a
    function of elapsed time steps (x-axis) on the same plot. You might find
    the helper function make_two_curve_plot helpful

    Args:
        num_bacteria (int): number of ResistantBacteria to create for
            the patient
        max_pop (int): maximum bacteria population for patient
        birth_prob (float int [0-1]): reproduction probability
        death_prob (float in [0, 1]): probability of a bacteria cell dying
        resistant (bool): whether the bacteria initially have
            antibiotic resistance
        mut_prob (float in [0, 1]): mutation probability for the
            ResistantBacteria cells
        num_trials (int): number of simulation runs to execute

    Returns: a tuple of two lists of lists, or two 2D arrays
        populations (list of lists or 2D array): the total number of bacteria
            at each time step for each trial; total_population[i][j] is the
            total population for trial i at time step j
        resistant_pop (list of lists or 2D array): the total number of
            resistant bacteria at each time step for each trial;
            resistant_pop[i][j] is the number of resistant bacteria for
            trial i at time step j
    """
    bacteria = []
    for i in range(0, num_bacteria):
        bacteria.append(ResistantBacteria(birth_prob, death_prob, resistant, mut_prob))
    print("Loading ", end="")
    populations = []
    resistant_population = []
    for i in range(0, num_trials):
        patient = TreatedPatient(bacteria.copy(), max_pop)
        nb_of_bacteria = []
        nb_of_resistant_bacteria = []
        time_steps1 = 150
        for time_step in range(0, time_steps1):
            nb_of_resistant_bacteria.append(patient.get_resist_pop())
            if time_step == 0:
                nb_of_bacteria.append(len(bacteria))
            else:
                nb_of_bacteria.append(patient.update())
        patient.set_on_antibiotic()
        time_steps2 = 250
        for time_step in range(0, time_steps2):
            nb_of_resistant_bacteria.append(patient.get_resist_pop())
            if time_step == 0:
                nb_of_bacteria.append(len(bacteria))
            else:
                nb_of_bacteria.append(patient.update())
        populations.append(nb_of_bacteria)
        resistant_population.append(nb_of_resistant_bacteria)
        print(".", end="")
    print(" Done")
    average_list_for_population = []
    average_list_for_resistant_bacteria = []
    x_coordinates = []
    time_steps = time_steps1 + time_steps2
    for n in range(0, time_steps):
        x_coordinates.append(n)
        average_list_for_population.append(calc_pop_avg(populations, n))
        average_list_for_resistant_bacteria.append(calc_pop_avg(resistant_population, n))
    make_two_curve_plot(x_coordinates, average_list_for_population, average_list_for_resistant_bacteria, "Total",
                        "Resistant", "Timestep", "Average Population",
                        "Average Bacteria Population per Timestep (With an Antibiotics)")
    return populations, resistant_population


# When you are ready to run the simulations, uncomment the next lines one at a time

# Simulation A
total_pop1, resistant_pop1 = simulation_with_antibiotic(num_bacteria=100, max_pop=1000, birth_prob=0.3, death_prob=0.2,
                                                        resistant=False, mut_prob=0.8, num_trials=50)

total_pop_95_conf_int = calc_95_ci(total_pop1, 299)
resistant_pop_95_conf_int = calc_95_ci(resistant_pop1, 299)
print("Simulation A")
print("For the total population: The mean =", total_pop_95_conf_int[0], ", and the confidence interval width =",
      total_pop_95_conf_int[1])
print("For the resistant population: The mean =", resistant_pop_95_conf_int[0], ", and the confidence interval width =",
      resistant_pop_95_conf_int[1])

# Simulation B
total_pop2, resistant_pop2 = simulation_with_antibiotic(num_bacteria=100, max_pop=1000, birth_prob=0.17, death_prob=0.2,
                                                        resistant=False, mut_prob=0.8, num_trials=50)

total_pop_95_conf_int = calc_95_ci(total_pop2, 299)
resistant_pop_95_conf_int = calc_95_ci(resistant_pop2, 299)
print("Simulation B")
print("For the total population: The mean =", total_pop_95_conf_int[0], ", and the confidence interval width =",
      total_pop_95_conf_int[1])
print("For the resistant population: The mean =", resistant_pop_95_conf_int[0], ", and the confidence interval width =",
      resistant_pop_95_conf_int[1])

##########################
# PROBLEM 6
##########################
#
# 1) In simulation A, before introducing the antibiotic the average total population starts by increasing and then
#    converges to a constant number.
#    In simulation B, before introducing the antibiotic the average total population increases until it reaches its peak
#    somewhere between 40 and 50 timesteps and then it starts to decrease.
#
# 2) In simulation A, before introducing the antibiotic the average resistant bacteria population starts by increasing
#    until it reaches a peak somewhere between 40 and 50 timesteps where it starts to decrease until it stabilize at
#    some minimum value.
#    In simulation B, before introducing the antibiotic the average resistant bacteria population increases until it
#    reaches its peak somewhere between 40 and 50 timesteps and then it starts to decrease.
#
# 3) In simulation A, after introducing the antibiotic the average total population increases slowly.
#    In simulation B, after introducing the antibiotic the average total population continue itd decease until it
#    reaches 0 and never changes again.
#
# 4) In both simulation A and B, after introducing the antibiotic the average resistant bacteria population starts by
#    exactly follow the total population.
#
