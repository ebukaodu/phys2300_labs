'''
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: weather.py

Usage: python datafile

Description: Code to analyze weather data

Inputs: name of data file containing weather data

Outputs: plots and analysis

Auxiliary Files: None

Special Instructions: None

Mordified by : Chukwuebuka Odu

Date: 2/14/2019

Project: Programming Assignment M3

Instruction: Use analysis of weather data from the Ogden area to explore how to read data from files and perform some
--------------------------------------------------------------------------------
'''
import sys
import numpy as np
import pandas as pd
import matplotlib.pylab as plt

# Pseudocode:
# 1) get the name of the data file from the user on the command line
# 2) open the data file
# 3) read the first line of data and throw it away (it is the header info the computer doesn't need)
#       from all the remaining lines:
#       read in the date (index 2) and temperature (index 3)
#       parse the date string into year, month, day
#       convert year, month, day into decimal years for plotting
# 4) make two lists for the time series - the decimal year list and the temperature list
# 5) sort the data by month so we can average it and take the standard deviation later
# 6) Plot the results

def parse_data(infile):
    """    
    Function to parse weather data
    :param infile: weather data input file
    :return: two lists. One list with the information from the third column (date)
                        One list with the information from the fourth column (temperature)
     """   
    wdates = []             # list of dates data
    wtemperatures = []      # list of temperarture data

    return wdates, wtemperatures


def calc_mean_std_dev(wdates, wtemp):
    """  
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param wdates: list with dates fields
    :param wtemp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """    
    means = []
    std_dev = []

    return means, std_dev



def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    A bar chart of the results for the climate graph
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per
    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """
    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Temperatures at Ogden")
    plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Daily Temperature, F")
    plt.xlabel("Year")

    plt.subplot(2, 1, 2)                # select second subplot
    plt.ylabel("Average Temperature, F")
    plt.xlabel("Year")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.7, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber, month_mean, yerr=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.show()      # display plot


def plot_data_task2(wyear, tempMin, tempMax):
    """
    Create plot for Task 2. Describe in here what you are plotting
    Also modify the function to take the params you think you will need
    to plot the requirements.
    :param: wyear: list with year 
    :param: tempMin: list with each year's min value
    :param: tempMax: list with each year's max value
    """
    plt.title("Minimum and Maximum Temperatures per year")
    plt.ylabel("Temperature, F")
    plt.xlabel("Year")
    plt.scatter(wyear, tempMax, s=40, marker= "*", c='r', label='Maximum Temp')
    plt.scatter(wyear, tempMin, s=40, marker= "*", c='b', label='Minimum Temp') 
    plt.legend()
    plt.show()      # display plot


def main(data):
    """
    "Main" Function
    This function uses pandas to parse weather data
    it is calling the plot_data_task1 fuction that creates the graphs
    Param: data -> data file
    """
    #weather_data = infile    # take data file as input parameter to file
    #wdates, wtemperatures = parse_data(weather_data)
    # Calculate mean and standard dev per month
    #month_mean, month_std = calc_mean_std_dev(wdates, wtemperatures)
    # TODO: Make sure you have a list of:
    #       1) years, 2) temperature, 3) month_mean, 4) month_std
    
    #geting the mean of temperature by month
    month_mean = data.groupby(data['Date'].dt.strftime('%m %B'))['TEMP'].mean()
    
    #geting the standard deviation of temperature by month
    month_std = data.groupby(data['Date'].dt.strftime('%m %B'))['TEMP'].std()

    #remove the number i.e s/n of month
    month_mean.index = [ x.split()[1] for x in month_mean.index ]
    month_std.index = [ x.split()[1] for x in month_std.index ]
    
    wyear = data['Date'].dt.year #getting the years
    wtemp = data['TEMP'] #getting the temperature
    
    #replace missing data with 0
    data.loc[data['TEMP'] == 9999.9] = 0
    data.loc[data['TEMP'] == 999.9] = 0
    
    #get the min and max temperature
    tempMin = data.groupby(data['Date'].dt.year)['TEMP'].min()
    tempMax = data.groupby(data['Date'].dt.year)['TEMP'].max()
    
    pyear = wyear.groupby(wyear).count()
    plot_data_task1(wyear, wtemp, month_mean.tolist(), month_std.tolist())
    # TODO: Create the data you need for this
    plot_data_task2(pyear.index.tolist(), tempMin.tolist(), tempMax.tolist())



if __name__ == "__main__":
    # infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    data = pd.read_fwf("data/CDO6674605799016.txt")
    data = data[["YEARMODA", "TEMP"]]
    
    #I don't like the date format, so I changed it to the standard date-time format
    data['Date'] = pd.to_datetime(data['YEARMODA'], format='%Y%m%d')
    main(data)
    exit(0)
