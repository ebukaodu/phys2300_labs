'''
Assignment to learn how to interpolate data1
'''
import sys
import matplotlib.pyplot as plt
import numpy as np
# import scipy
import pandas as pd
import datetime as dt

#https://youtu.be/-zvHQXnBO6c
def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    pass


def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    pass


def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with four lists:
        1) wx correlated altitude up
        2) wx correlated temperature up
        3) wx correlated altitude down
        4) wx correlated temperature down
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    pass


def plot_figs(TempPressure,tem):
    """
    Plot 2 figures with 2 subplots each.
    :param TempPressure: A dictionary to collect data.
    :param tem: A dictionary to collect data for Ascension & Descension Altitude
    :return: nothing
    """
    # Elapse time vs temperature  plot
    plt.figure()
    plt.subplot(2, 1, 1)
    plt.title("Harbor flight data")
    plt.ylabel("Tempature, F")
    plt.plot(TempPressure["TempPress_times"], TempPressure["Ch1:Deg F"])
    plt.ylim(-60,80)
    plt.xlim(0, 2.5)

    #Altitude vs elapse time plot
    plt.subplot(2, 1, 2)
    plt.ylabel("Alititude, ft")
    plt.xlabel("Mission elapsed Time, Hours")
    plt.plot(TempPressure['GPSData-Time-In-Hours'], TempPressure['GPSData-ALT'])
    plt.xlim(0, 2.5)
    plt.ylim(0, 100000)
    plt.show()

    #Temperature vs Ascension Altitude plot
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.title("Harbor Ascent Flight Data")
    plt.ylabel("Altitude feet")
    plt.xlabel("Temperature, F")
    plt.plot(tem['TempPressure_up'], tem['GPSData-ALT-up'])
    plt.xlim(-40, 80)
    plt.ylim(0,100000)

    #Temperature vs descension Altitude plot
    plt.subplot(1, 2, 2)
    plt.title("Harbor Descent Flight Data")
    #plt.ylabel("Altitude feet")
    plt.xlabel("Temperature, F")
    plt.plot(tem['TempPressure_down'], tem['GPSData-ALT-down'])
    plt.xlim(-60, 80)
    plt.ylim(0,100000)
    plt.show()


def main(TempP,GPS):
    """
    Main function
    Param: TempPressure -> data file
    Param: GPSData -> data file
    :return: Nothing
    """
    col = ["GPS HOURS", "MIN", "SEC", "MET (MIN)", "LONG (decimal deg)", "LAT (decimal deg)", "ALT (ft)"]

    GPSData = pd.read_csv(GPS, sep='\t', names = col, header=0, skiprows=range(0, 1))

    TempPressure = pd.read_csv(TempP)

    TempPressure = TempPressure[["Time", "Ch1:Deg F"]]
    GPSData = GPSData[["GPS HOURS", "MIN", "SEC", "ALT (ft)"]]
    
    tem = {}
    #Temp = sys.argv[1]                   # first program input param
    #GPS = sys.argv[2]                  # second program input param

    tem['TempPress_times'] = []
    tem['GPSData-ALT-up'] = []
    tem['GPSData-ALT-down'] = []
    tem["TempPressure_up"] = []
    tem["TempPressure_down"] = []
    
    #read_wx_data(wx_file, harbor_data)      # collect weather data
    #read_gps_data(gps_file, harbor_data)    # collect gps data
    #interpolate_wx_from_gps(harbor_data)    # calculate interpolated data

    temp = list(TempPressure["Time"])
    for t in temp:
        delta_t = dt.datetime.strptime(t, '%H:%M:%S') - dt.datetime.strptime(temp[0], '%H:%M:%S')
        tem['TempPress_times'].append(float(delta_t.total_seconds()/3600))

    TempPressure['TempPress_times'] = tem['TempPress_times']

    GPSData['seconds'] = (GPSData['GPS HOURS'] * 3600 + GPSData['MIN'] * 60 + GPSData['SEC'])

    ms_Time = GPSData['GPS HOURS'][0] * 3600 + GPSData['MIN'][0] * 60 + GPSData['SEC'][0]
    TempPressure['GPSData-Time-In-Hours'] = (GPSData['seconds'] - ms_Time) / 3600
    TempPressure["GPSData-ALT"] = GPSData[['ALT (ft)']]

    # GPS Data for ALT ascension
    np.set_printoptions(threshold=np.inf)
    tem['GPSData-ALT-up']  = np.linspace(GPSData['ALT (ft)'][0], GPSData['ALT (ft)'].max(), 1945)
    #TempPressure['GPSData-ALT-up'] = tem['GPSData-ALT-up']
    tem["TempPressure_up"] = TempPressure["Ch1:Deg F"][0:1945]

    # GPS Data for ALT descension
    tem["GPSData-ALT-down"] = np.linspace(GPSData['ALT (ft)'].max(), GPSData['ALT (ft)'].min(), 1063)
    #TempPressure["GPSData-ALT-down"] = tem["GPSData-ALT-down"]
    tem["TempPressure_down"] = TempPressure["Ch1:Deg F"][1946:3009]

    plot_figs(TempPressure,tem)                  # display figures


if __name__ == '__main__':
    Temp = 'TempPressure.txt'  
    GPSData = 'GPSData.txt'
    
    main(Temp,GPSData)
    exit(0)
