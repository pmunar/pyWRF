import os

class RunAnalysis:
    def __init__(self,group_start_date, group_end_date, path_do_input_data, path_to_output_data, run_hours=120,
                 hour_step=6):

    self.start_date = group_start_date   # datetime object format
    self.end_date = group_end_date       # datetime object format
    self.analysis_interval = self.end_date - self.start_date
    self.input_data = path_do_input_data
    self.ouput = path_to_output_data
    self.run_hours = self.analysis_interval.days * 24
    self.hour_step = hour_step
    self.interval_seconds = self.hour_step * 3600.

    self.WRF_DIR = get_wrf_dir()
    self.WORK_DIR = os.getcwd()
    self.namelist_in = open(self.WRF_DIR+'/WPS/namelist.wps', 'r')

    def _write_times_field(self, line, date):
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        date_to_write = '{:d}-{:02d}-{:02d}_{:02d}:00:00'.format(year, month, day, hour)
        date_field = line.split('=')
        date_field[1] = date_to_write + "','" + date_to_write + "','" + date_to_write
        new_line = date_field[0] + " = '" + date_field[1] + "',"
        return new_line


    def _change_WPS_namelist_input_file(self):
        namelist_out = open(self.WRF_DIR + '/WPS/temp_namelist.wps', 'w')
        lines = self.namelist_in.readlines()
        lines[3] = self._write_times_field(lines[3], self.start_date)
        lines[4] = self._write_times_field(lines[4], self.end_date)
        for l in lines:
            print(l[:-1], file=namelist_out)
        namelist_out.close()
        os.system('mv '+namelist_out.name+' '+self.namelist_in.name)


    def _link_input_data_to_WPS(self):
        from lib.read_config import datetime_to_filename_format
        date = self.start_date
        while date <= self.end_date:
            date_filename_format = datetime_to_filename_format(date)
            infile = 'fnl_%s.grib2'%(date_filename_format)
            os.system('ln -s '+infile+' $WRF_DIR/DATA')
            date += dt.timedelta(hours=self.hour_step)


    def run_wps(self):
        from lib.read_config import working_directory
        self._change_WPS_namelist_input_file()
        self._link_input_data_to_WPS()

        with working_directory(self.WRF_DIR+'/WPS'):
            print('We moved to '+os.getcwd())
            os.system('./geogrid.exe >& log.geogrid')
            try:
                log_geogrid = open('log.geogrid')
                success_string = 'Successful completion of geogrid'
                if success_string in log_geogrid.readlines():
                    print('Geodrid ended successfully!')
                else:
                    print('Geogrid ended without success. Check log file')
            except:
                print('Geogrid did not generate log file')

            os.system('ln -sf ungrib/Variable_Tables/Vtable.GFS '+self.WRF_DIR+'/WPS/Vtabl')
            os.system('./WPS/link_grib.csh '+self.WRF_DIR+'/DATA/fnl_')
            os.system('./WPS/ungrib.exe >& ungrib_data.log')
            os.system('./WPS/metgrid.exe >& log.metgrid')

            try:
                log_metgrid = open('log.metgrid')
                success_string = 'Successful completion of metgrid'
                if success_string in log_metgrid.readlines():
                    print('metgrid ended successfully!')
                else:
                    print('metgrid ended without success. Check log file')
            except:
                print('metgrid did not generate log file')
        print('We went back to '+os.getcwd())

    def _change_WRF_namelist_input_file(self):

        namelist_wrf_in = open(self.WRF_DIR+'/WRF3/test/em_real/namelist.input')
        namelist_wrf_out = open(self.WRF_DIR+'/WRF3/test/em_real/temp_namelist.input', 'w')

        lines = namelist_wrf_in.readlines()

        lines[2].split('=')[1] = str(self.run_hours)+','
        lines[5].split('=')[1] = str(self.start_date.year)+',' + str(self.start_date.year)+',' \
                                 + str(self.start_date.year)+','
        lines[6].split('=')[1] = str(self.start_date.month)+',' + str(self.start_date.month)+',' \
                                 + str(self.start_date.month)+','
        lines[7].split('=')[1] = str(self.start_date.day) + ',' + str(self.start_date.day) + ',' \
                                 + str(self.start_date.day) + ','
        lines[8].split('=')[1] = str(self.start_date.hour) + ',' + str(self.start_date.hour) + ',' \
                                 + str(self.start_date.hour) + ','
        lines[11].split('=')[1] = str(self.end_date.year) + ',' + str(self.end_date.year) + ',' \
                                 + str(self.end_date.year) + ','
        lines[12].split('=')[1] = str(self.end_date.month) + ',' + str(self.end_date.month) + ',' \
                                 + str(self.end_date.month) + ','
        lines[13].split('=')[1] = str(self.end_date.day) + ',' + str(self.end_date.day) + ',' \
                                 + str(self.end_date.day) + ','
        lines[14].split('=')[1] = str(self.end_date.hour) + ',' + str(self.end_date.hour) + ',' \
                                 + str(self.end_date.hour) + ','
        lines[15].split('=')[1] = str(self.interval_seconds)+','

        for l in lines:
            print(l[:-1], file=namelist_wrf_out)
        os.system('mv ' + namelist_wrf_out.name + ' ' + namelist_wrf_in.name)

    def run_WRF(self):
        from lib.read_config import working_directory
        with working_directory(self.WRF_DIR+'WRFV3/test/em_real'):
            print('Moving to ' + os.getcwd())
            os.system('ln -sf '+self.WRF_DIR+'/WPS/met_em* .')
            self._change_WRF_namelist_input_file()
            os.system('./real.exe')
            date_string = str(self.start_date).split(' ')
            date_string_WRF = date_string[0]+'_'+date_string[1]
            try:
                if os.path.isfile(self.WRF_DIR+'/WRFV3/test/em_real/wrfinput_d01') and os.stat(
                            self.WRF_DIR+'/WRFV3/test/em_real/wrfinput_d01').st_size != 0:
                    print('wrfinput_d01 created successfully')
                if os.path.isfile(self.WRF_DIR + '/WRFV3/test/em_real/wrfinput_d02') and os.stat(
                            self.WRF_DIR + '/WRFV3/test/em_real/wrfinput_d02').st_size != 0:
                    print('wrfinput_d02 created successfully')
                if os.path.isfile(self.WRF_DIR + '/WRFV3/test/em_real/wrfinput_d03') and os.stat(
                            self.WRF_DIR + '/WRFV3/test/em_real/wrfinput_d03').st_size != 0:
                    print('wrfinput_d03 created successfully')
                if os.path.isfile(self.WRF_DIR + '/WRFV3/test/em_real/wrfbdy_d01') and os.stat(
                            self.WRF_DIR + '/WRFV3/test/em_real/wrfbdy_d01').st_size != 0:
                print('wrfbdy_d01 created successfully')
            except:
                print('something went wrong. Files not created or with zero size')

            os.system('. $WRF_DIR/WRFV3/test/em_real/wrf.exe')
            try:
                if os.path.isfile(self.WRF_DIR+'/WRFV3/test/em_real/wrfout_d01_'+date_string_WRF) and os.stat(
                            self.WRF_DIR+'/WRFV3/test/em_real/wrfout_d01_'+date_string_WRF).st_size != 0:
                    print('wrfout_d01 created successfully')
                if os.path.isfile(self.WRF_DIR + '/WRFV3/test/em_real/wrfout_d02_'+date_string_WRF) and os.stat(
                            self.WRF_DIR + '/WRFV3/test/em_real/wrfout_d02_'+date_string_WRF).st_size != 0:
                    print('wrfout_d02 created successfully')
                if os.path.isfile(self.WRF_DIR + '/WRFV3/test/em_real/wrfout_d03_'+date_string_WRF) and os.stat(
                            self.WRF_DIR + '/WRFV3/test/em_real/wrfout_d03_'+date_string_WRF).st_size != 0:
                print('wrfout_d03 created successfully')
            except:
                print('something went wrong. Output WRF Files not created or with zero size')
        print('We went back to ' + os.getcwd())

