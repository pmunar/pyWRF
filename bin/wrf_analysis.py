#!/usr/bin/env python
import datetime
import sys
import argparse

from pyWRF.run_analysis import RunAnalysis
from pyWRF.read_config import get_config_parameters
from pyWRF.utils import conf_date_to_datetime
from pyWRF.read_and_unzip import gunzip_and_rename_files


def check_length_of_analysis(start_date, end_date):
    """
    Function to check the length, in days and hours, of the analysis that will be performed
    :param start_date: datetime object
    :param end_date: datetime object
    :return: delta.days, delta.seconds//3600.
    """
    delta = end_date - start_date
    return delta.days, delta.seconds//3600.


def get_stop_date_for_processing(start_date, group_of_days):
    """
    Function that returns the stop_date for the next group of days of the analysis. This is used when the analysis
    interval is too long and we divide it into few days analysis group.
    :param start_date: datetime object representing the start date of the group of analysis
    :param group_of_days: integer representing the length of the group of days that will be analyzed at once
    :return: datetime object representing the stop date of the group of days to be analyzed
    """
    stop_time = start_date + datetime.timedelta(days=group_of_days - 1, hours=18)
    return stop_time

def get_stop_date_for_processing_last_group(end_date):
    """
    Function that returns the stop_date for the next group of days of the analysis. This is used when the analysis
    interval is too long and we divide it into few days analysis group. This function is called when we are at the
    last group of days, and it returns the end_date parameter as the output
    :param end_date:
    :return:
    """
    stop_time = end_date
    return stop_time

# The next lines are the main section of this python script. Here we load the config file,
# we parse it and we can introduce optional parameters for the analysis, in case we want just
# to run a part of the analysis (being wps, wrf, grads or clean the optional parameters).

# The program divides the total elapsed time of analysis we want to perform in smaller groups
# of time, of the lenght specified in the configuration file.

parser = argparse.ArgumentParser()
parser.add_argument('config', help='the configuration file to run the analysis')
parser.add_argument('--wps', help="if selected, this option makes the program to compute only the WPS outputs",
                    action='store_true')
parser.add_argument('--wrf', help="if selected, this option makes the program to compute only the WRF outputs",
                    action='store_true')
parser.add_argument('--grads', help="if selected, this option makes the program to compute only the GRADS outputs",
                    action='store_true')
parser.add_argument('--clean', help="if selected, this option makes the program only to clean the directories",
                    action='store_true')
args = parser.parse_args()

data_path, output_path, data_format, start_date, end_date, group = get_config_parameters(args.config)

print('=========================================================')
print('                     Summary')
print('=========================================================')
print('Path to the data:{}'.format(data_path))
print('Path to the WPS output:{}/wps_out'.format(output_path))
print('Path to the WRF output:{}/wrf_out'.format(output_path))
print('Path to the GRADS output:{}/grads_out'.format(output_path))
print('Starting date of analysis:{}'.format(start_date))
print('Ending date of analysis:{}'.format(end_date))
print('Days in each subgroup of analysis:{}'.format(group))
print('=========================================================')
print('=========================================================')

print('Unzipping files...')
gunzip_and_rename_files(data_path, data_format)
start_date_datetime = conf_date_to_datetime(start_date)
end_date_datetime = conf_date_to_datetime(end_date)
length_of_analysis = check_length_of_analysis(start_date_datetime, end_date_datetime)

print('The total time of the analysis is {} days {} hours'.format(length_of_analysis[0], length_of_analysis[1]))

number_of_groups = divmod(length_of_analysis[0], group)

start_time = start_date_datetime
for n in range(number_of_groups[0] + 1):
    stop_time = get_stop_date_for_processing(start_time, group)
    if n == range(number_of_groups[0] + 1)[-1]:
        stop_time = get_stop_date_for_processing_last_group(end_date_datetime)
    print('Group {}'.format(n +1))
    print('Analyzing times between {} and {}'.format(start_time, stop_time))
    analysis = RunAnalysis(start_time, stop_time, data_path, output_path, data_format)

    if args.wps:
        analysis.run_wps()
        start_time = stop_time + datetime.timedelta(hours=6)
        continue
    elif args.wrf:
        analysis.run_WRF()
        start_time = stop_time + datetime.timedelta(hours=6)
        continue
#    elif args.grads:
#        analysis.run_grads()
#        start_time = stop_time + datetime.timedelta(hours=6)
#        continue
    elif args.clean:
        analysis.clean_directories()
        start_time = stop_time + datetime.timedelta(hours=6)
        continue
    elif args.wps and args.wrf:
        analysis.run_wps()
        analysis.run_WRF()
        start_time = stop_time + datetime.timedelta(hours=6)
        continue
    else:
        analysis.run_wps()
        analysis.run_WRF()
        analysis.clean_directories()
        start_time = stop_time + datetime.timedelta(hours=6)

