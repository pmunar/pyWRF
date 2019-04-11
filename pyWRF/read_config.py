from contextlib import contextmanager
import os

def get_config_parameters(config_file):
    import configparser
    Config = configparser.ConfigParser()
    Config.read(config_file)
    Config.sections()
    start_date = Config.get('Analysis', 'start_date')[1:-1]
    end_date = Config.get('Analysis', 'end_date')[1:-1]
    group_of_days = Config.get('Analysis', 'group_of_days')
    data_path = Config.get('Data', 'data_path')
    out_wps = Config.get('Data', 'wps_out')[1:-1]
    out_wrf = Config.get('Data', 'wrf_out')[1:-1]
    out_grads = Config.get('Data', 'grads_out')[1:-1]

    return data_path, out_wps, out_wrf, out_grads, start_date, end_date, int(group_of_days)

def conf_date_to_datetime(conf_date):
    import datetime
    cd_split = conf_date.split('-')
    cd_year, cd_month = int(cd_split[0]), int(cd_split[1])
    cd_day_hh_mm_split = cd_split[2].split('_')
    cd_day, cd_hour, cd_min = int(cd_day_hh_mm_split[0]), int(cd_day_hh_mm_split[1]), int(cd_day_hh_mm_split[2])

    conf_datetime = datetime.datetime(cd_year, cd_month, cd_day, cd_hour, cd_min)
    return conf_datetime


def datetime_to_filename_format(date):
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour

    date_string = '{:d}{:02d}{:02d}_{:02d}_00'.format(year, month, day, hour)
    return date_string


@contextmanager
def working_directory(directory):
    owd = os.getcwd()
    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(owd)

# start_date_datetime = conf_date_to_datetime(start_date)
# end_date_datetime = conf_date_to_datetime(end_date)
#
# length_of_analysis = end_date_datetime - start_date_datetime
# print('Length of the analysis: {:d} days'.format(length_of_analysis.days))
