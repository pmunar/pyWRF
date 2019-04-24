#!/usr/bin/env python
import datetime
import sys

from pyWRF.run_analysis import RunAnalysis
from pyWRF.read_config import get_config_parameters
from pyWRF.utils import conf_date_to_datetime
from pyWRF.read_and_unzip import gunzip_and_rename_files


def check_length_of_analysis(start_date, end_date):
    delta = end_date - start_date
    return delta.days, delta.seconds//3600.


def get_stop_date_for_processing(start_date, group_of_days):
    stop_time = start_date + datetime.timedelta(days=group_of_days - 1, hours=18)
    return stop_time

def get_stop_date_for_processing_last_group(end_date):
    stop_time = end_date
    return stop_time


data_path, output_path, start_date, end_date, group = get_config_parameters(sys.argv[1])

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
gunzip_and_rename_files(data_path)
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
    analysis = RunAnalysis(start_time, stop_time, data_path, output_path)
    analysis.run_wps()
    analysis.run_WRF()
    analysis.clean_directories()

    start_time = stop_time + datetime.timedelta(hours=6)

