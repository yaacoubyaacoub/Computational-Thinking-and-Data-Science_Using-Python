# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Yaacoub Yaacoub
# Time:

import pylab
import math
import re

# cities in our weather data
CITIES = ['BOSTON', 'SEATTLE', 'SAN DIEGO', 'PHILADELPHIA', 'PHOENIX', 'LAS VEGAS', 'CHARLOTTE', 'DALLAS', 'BALTIMORE',
          'SAN JUAN', 'LOS ANGELES', 'MIAMI', 'NEW ORLEANS', 'ALBUQUERQUE', 'PORTLAND', 'SAN FRANCISCO', 'TAMPA',
          'NEW YORK', 'DETROIT', 'ST LOUIS', 'CHICAGO']

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""


class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """

    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]


def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y) ** 2).sum()
    var_x = ((x - x.mean()) ** 2).sum()
    SE = pylab.sqrt(EE / (len(x) - 2) / var_x)
    return SE / model[0]


"""
End helper code
"""


def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for d in degs:
        model = pylab.polyfit(x, y, d)
        models.append(model)
    return models


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.

    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    assert len(y) == len(estimated), "the number of predicted values does not match the number of observed values "
    error = ((y - estimated) ** 2).sum()
    y_mean = y.mean()
    variability = ((y - y_mean) ** 2).sum()
    return 1 - error / variability


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    pylab.plot(x, y, 'bo', label="Data")
    for i in range(len(models)):
        estimated_y = pylab.polyval(models[i], x)
        error = r_squared(y, estimated_y)
        if len(models[i]) == 2:
            s_e_o_v = se_over_slope(x, y, estimated_y, models[i])
            pylab.plot(x, estimated_y,
                       label="fit of degree " + str(len(models[i]) - 1) + ", R2 = " + str(round(error, 5))
                             + ",\nStandard Error Over Slope = " + str(round(s_e_o_v, 5)))
        else:
            pylab.plot(x, estimated_y, label="fit of degree " + str(len(models[i]) - 1)
                                             + ", R2 = " + str(round(error, 5)))
        pylab.legend()
        pylab.title("Variation of the temperature over the years in some US cities")
        pylab.xlabel("Years")
        pylab.ylabel("Temperature (in degree Celsius)")
    pylab.show()


# Testing evaluate_models_on_training function:
# x = pylab.array(range(2000, 2016))
# y = pylab.array([30,30,30,31,31,31,32,32,32,31,30,30,29,28,28,27])
# degrees = [1, 2, 4, 16]
# models = generate_models(x, y, degrees)
# evaluate_models_on_training(x, y, models)

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    yearly_average_temp = []
    for y in years:
        this_year_average_temp = 0
        for city in multi_cities:
            this_year_average_temp += climate.get_yearly_temp(city, y).mean()
        this_year_average_temp = this_year_average_temp / len(multi_cities)
        yearly_average_temp.append(this_year_average_temp)
    yearly_average_temp = pylab.array(yearly_average_temp)
    return yearly_average_temp


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    new_y = []
    for i in range(len(y)):
        sum = 0
        if i + 1 <= window_length:
            for j in range(i + 1):
                sum += y[j]
            average = sum / (i + 1)
        elif i + 1 >= window_length:
            for j in range(i + 1 - window_length, i + 1):
                sum += y[j]
            average = sum / window_length
        new_y.append(round(average, 2))
    new_y = pylab.array(new_y)
    return new_y


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    RMSE = math.sqrt((((y - estimated) ** 2).sum()) / len(y))
    return RMSE


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual
        city temperatures for the given cities in a given year.
    """
    yearly_temp_sd = []
    for y in years:
        daily_average_temp = []
        for month in range(1, 13):
            if month in [1, 3, 5, 7, 8, 10, 12]:
                for day in range(1, 32):
                    temp = 0
                    for city in multi_cities:
                        temp += climate.get_daily_temp(city, month, day, y)
                    daily_average_temp.append(temp / len(multi_cities))
            elif month in [4, 6, 9, 11]:
                for day in range(1, 31):
                    temp = 0
                    for city in multi_cities:
                        temp += climate.get_daily_temp(city, month, day, y)
                    daily_average_temp.append(temp / len(multi_cities))
            elif month == 2:
                if y % 4 == 0:
                    for day in range(1, 30):
                        temp = 0
                        for city in multi_cities:
                            temp += climate.get_daily_temp(city, month, day, y)
                        daily_average_temp.append(temp / len(multi_cities))
                else:
                    for day in range(1, 29):
                        temp = 0
                        for city in multi_cities:
                            temp += climate.get_daily_temp(city, month, day, y)
                        daily_average_temp.append(temp / len(multi_cities))
        yearly_temp_sd.append(pylab.std(daily_average_temp))
    yearly_temp_sd = pylab.array(yearly_temp_sd)
    return yearly_temp_sd


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    pylab.plot(x, y, 'bo', label="Data")
    for i in range(len(models)):
        estimated_y = pylab.polyval(models[i], x)
        error = rmse(y, estimated_y)
        pylab.plot(x, estimated_y, label="fit of degree " + str(len(models[i]) - 1) + ", R2 = " + str(round(error, 5)))
        pylab.legend()
        pylab.title("Variation of the temperature over the years in some US cities")
        pylab.xlabel("Years")
        pylab.ylabel("Temperature (in degree Celsius)")
    pylab.show()


if __name__ == '__main__':
    pass
    # Part A.4
    # Data = Climate("data.csv")
    # Year = pylab.array(TRAINING_INTERVAL)
    # temp_on_jan10 = []
    # for year in TRAINING_INTERVAL:
    #     temp_on_jan10.append(Data.get_daily_temp("NEW YORK", 1, 10, year))
    # temp_on_jan10 = pylab.array(temp_on_jan10)
    # models_A1 = generate_models(Year, temp_on_jan10, [1])
    # evaluate_models_on_training(Year, temp_on_jan10, models_A1)
    #
    # average_yearly_temp = []
    # for year in TRAINING_INTERVAL:
    #     average_yearly_temp.append(Data.get_yearly_temp("NEW YORK", year).mean())
    # average_yearly_temp = pylab.array(average_yearly_temp)
    # models_A2 = generate_models(Year, average_yearly_temp, [1])
    # evaluate_models_on_training(Year, average_yearly_temp, models_A2)

    # Part B
    # Data = Climate("data.csv")
    # Year = pylab.array(TRAINING_INTERVAL)
    # average_yearly_temp = gen_cities_avg(Data, CITIES, Year)
    # models_B = generate_models(Year, average_yearly_temp, [1])
    # evaluate_models_on_training(Year, average_yearly_temp, models_B)

    # Part C
    # Data = Climate("data.csv")
    # Year = pylab.array(TRAINING_INTERVAL)
    # average_yearly_temp = gen_cities_avg(Data, CITIES, Year)
    # average_yearly_temp = moving_average(average_yearly_temp, 5)
    # models_C = generate_models(Year, average_yearly_temp, [1])
    # evaluate_models_on_training(Year, average_yearly_temp, models_C)

    # Part D.2
    # Data = Climate("data.csv")
    # Training_Years = pylab.array(TRAINING_INTERVAL)
    # average_yearly_temp = gen_cities_avg(Data, CITIES, Training_Years)
    # average_yearly_temp = moving_average(average_yearly_temp, 5)
    # models_D = generate_models(Training_Years, average_yearly_temp, [1, 2, 20])
    # evaluate_models_on_training(Training_Years, average_yearly_temp, models_D)
    # Testing_Years = pylab.array(TESTING_INTERVAL)
    # average_yearly_temp_test = gen_cities_avg(Data, CITIES, Testing_Years)
    # average_yearly_temp_test = moving_average(average_yearly_temp_test, 5)
    # evaluate_models_on_testing(Testing_Years, average_yearly_temp_test, models_D)

    # Part E
    # Data = Climate("data.csv")
    # Training_Years = pylab.array(TRAINING_INTERVAL)
    # Training_sd = gen_std_devs(Data, CITIES, Training_Years)
    # average_sd_5years = moving_average(Training_sd, 5)
    # models_E = generate_models(Training_Years, Training_sd, [1])
    # evaluate_models_on_training(Training_Years, Training_sd, models_E)
