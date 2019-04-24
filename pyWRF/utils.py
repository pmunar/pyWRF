def conf_date_to_datetime(conf_date):
    """
    Function that converts the date from the config file, in string format, into datetime.datetime object
    :param conf_date: string
    :return: datetime object corresponding to the conf_date parameter
    """
    import datetime
    cd_split = conf_date.split('-')
    cd_year, cd_month = int(cd_split[0]), int(cd_split[1])
    cd_day_hh_mm_split = cd_split[2].split('_')
    cd_day, cd_hour, cd_min = int(cd_day_hh_mm_split[0]), int(cd_day_hh_mm_split[1]), int(cd_day_hh_mm_split[2])

    conf_datetime = datetime.datetime(cd_year, cd_month, cd_day, cd_hour, cd_min)
    return conf_datetime


def datetime_to_filename_format(date):
    """
    Returns a string corresponding to the date parameter
    :param date: datetime object
    :return: string
    """
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour

    date_string = '{:d}{:02d}{:02d}_{:02d}_00'.format(year, month, day, hour)
    return date_string

from contextlib import contextmanager
import os
@contextmanager
def working_directory(directory):
    """
    Moves to the directory path
    :param directory: string
    :return:
    """
    owd = os.getcwd()
    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(owd)