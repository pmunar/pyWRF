from read_config import get_config_parameters

from lib.read_and_unzip import gunzip_and_rename_files

start_date, end_date, group_of_days = get_config_parameters('/home/pmunar/Dropbox/pyWRF/test_data/conf.conf')

gunzip_and_rename_files('/home/pmunar/Dropbox/pyWRF/test_data')


def get_new_start_stop_for_processing(start_date):
    stop_time = start_date + dt.timedelta(days=self.maxgroupdays - 1, hours=18)
    new_start = stop_time + dt.timedelta(hours=6)
    return stop_time, new_start