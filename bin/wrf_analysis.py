
import sys
from pyWRF.read_config import get_config_parameters, conf_date_to_datetime
from pyWRF.read_and_unzip import gunzip_and_rename_files
from pyWRF.run_analysis import RunAnalysis
import datetime

def check_length_of_analysis(start_date, end_date):
    delta = end_date - start_date
    return delta.days, delta.seconds//3600.


def get_stop_date_for_processing(start_date, group_of_days):
    stop_time = start_date + datetime.timedelta(days=group_of_days - 1, hours=18)
    return stop_time

def get_stop_date_for_processing_last_group(end_date):
    stop_time = end_date
    return stop_time


def __main__():

    data_path, wps_out, wrf_out_grads_out, start_date, end_date, group = get_config_parameters(sys.argv[1])
    gunzip_and_rename_files()
    start_date_datetime = conf_date_to_datetime(start_date)
    end_date_datetime = conf_date_to_datetime(end_date)
    length_of_analysis = check_length_of_analysis(start_date_datetime, end_date_datetime)
    print('The total time of the analysis is {:d} days {:d} hours'.format(length_of_analysis[0], length_of_analysis[1]))
    number_of_groups = divmod(length_of_analysis[0], group)

    start_time = start_date_datetime
    for n in range(number_of_groups[0] + 1):
        stop_time = get_stop_date_for_processing(start_time, group)
        if n == range(number_of_groups[0] + 1)[-1]:
            stop_time = get_stop_date_for_processing_last_group(end_date_datetime)
        analysis = RunAnalysis(start_time, stop_time, )

        print('Analyzing times between +'start_time, stop_time, data_path, wps_out)
        start_time = stop_time + datetime.timedelta(hours=6)

