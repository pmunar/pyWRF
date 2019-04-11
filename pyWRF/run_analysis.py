import datetime
import os
import sys
from pyWRF.utils import working_directory
from pyWRF import environ


class RunAnalysis:
    def __init__(self,group_start_date, group_end_date, path_do_input_data, path_to_output_data, server='GDAS',
                 hour_step=6):

        self.start_date = group_start_date   # datetime object format
        self.end_date = group_end_date       # datetime object format
        self.analysis_interval = self.end_date - self.start_date
        self.input_data = path_do_input_data
        self.ouput = path_to_output_data
        self.run_hours = self.analysis_interval.total_seconds() // 3600 + hour_step
        self.hour_step = hour_step
        self.interval_seconds = int(self.hour_step * 3600.)
        self.server = server

        self.WRF_DIR = environ.DIRS.get('WRF_DIR')
        self.WORK_DIR = self.ouput

    def _write_new_text_for_line_wps(self, field, value):
        if type(value) == datetime.datetime:
            year = value.year
            month = value.month
            day = value.day
            hour = value.hour
            date_to_write = '{:d}-{:02d}-{:02d}_{:02d}:00:00'.format(year, month, day, hour)
            date_field = date_to_write + "','" + date_to_write + "','" + date_to_write
            new_line = ' ' + field + " = '" + date_field + "',\n"
            return new_line
        elif type(value) == int or type(value) == float:
            new_line = ' ' + field + " = " + str(value) + ',\n'
            return new_line

    def _write_new_text_for_line_wrf(self, field, value):
        if field == 'start_year':
            field_to_write = ' {:s}                          = {:d}, {:d}, {:d},\n'.format(field, value.year,
                                                                                           value.year, value.year)
        if field == 'start_month':
            field_to_write = ' {:s}                         = {:02d}, {:02d}, {:02d},\n'.format(field, value.month,
                                                                                                value.month, value.month)
        if field == 'start_day':
            field_to_write = ' {:s}                           = {:02d}, {:02d}, {:02d},\n'.format(field, value.day,
                                                                                                  value.day, value.day)
        if field == 'start_hour':
            field_to_write = ' {:s}                          = {:02d}, {:02d}, {:02d},\n'.format(field, value.hour,
                                                                                                 value.hour, value.hour)
        if field == 'end_year':
            field_to_write = ' {:s}                            = {:d}, {:d}, {:d},\n'.format(field, value.year,
                                                                                             value.year, value.year)
        if field == 'end_month':
            field_to_write = ' {:s}                           = {:02d}, {:02d}, {:02d},\n'.format(field, value.month,
                                                                                                  value.month, value.month)
        if field == 'end_day':
            field_to_write = ' {:s}                             = {:02d}, {:2d}, {:02d},\n'.format(field, value.day,
                                                                                                   value.day, value.day)
        if field == 'end_hour':
            field_to_write = ' {:s}                            = {:02d}, {:02d}, {:02d},\n'.format(field, value.hour,
                                                                                                   value.hour, value.hour)
        if field == 'interval_seconds':
            field_to_write = ' {:s}                    = {:d},\n'.format(field, value)
        try:
            return field_to_write
        except:
            print('could not rewrite namelist.input file')

    def _replacefield(self, file, searchExp, replaceExp):
        import fileinput
        for line in fileinput.FileInput(file, inplace=1):
            if searchExp in line:
                line = line.replace(line, replaceExp)
            sys.stdout.write(line)

    def _change_WPS_namelist_input_file(self):
        fields = ['start_date', 'end_date', 'interval_seconds']
        values = [self.start_date, self.end_date, self.interval_seconds]
        for f, v in zip(fields, values):
            self._replacefield(self.WRF_DIR + '/WPS/namelist.wps', f, self._write_new_text_for_line_wps(f, v))

    def _link_input_data_to_WPS(self):
        from pyWRF.utils import datetime_to_filename_format
        date = self.start_date
        while date <= self.end_date:
            date_filename_format = datetime_to_filename_format(date)
            infile = 'fnl_%s.grib2'%(date_filename_format)
            os.system('ln -s '+infile+' $WRF_DIR/DATA')
            date += datetime.timedelta(hours=self.hour_step)

    def _link_vtables(self):
        if self.server == 'GDAS' or self.server == 'GFS':
            vtable = 'Vtable.GFS'
        elif self.server == 'ERA-Interim' or self.server == 'ECMWF':
            vtable = 'Vtable.ECMWF'
        cwd = os.getcwd()
        os.system('ln -sf '+cwd+'ungrib/Variable_Tables/'+vtable+' '+cwd+'/Vtabl')

    def run_wps(self):
        self._change_WPS_namelist_input_file()
        self._link_input_data_to_WPS()

        print('Starting PREPROCESSING. This might take a while')
        if not os.path.exists(self.WORK_DIR + '/wps_out'):
            os.makedirs(self.WORK_DIR + '/wps_out')

        with working_directory(self.WRF_DIR+'/WPS'):
            print('We moved to '+os.getcwd())
            print('Running geogrid.exe')
            os.system('./geogrid.exe >& log.geogrid')
            try:
                log_geogrid = open('log.geogrid')
                success_string = 'Successful completion of geogrid'
                if success_string in log_geogrid.readlines():
                    print('Geodrid ended successfully!')
                else:
                    print('Geogrid ended without success. Check log file')
                    sys.exit()
            except:
                print('Geogrid did not generate log file')
                sys.exit()

            self._link_vtables()
            os.system('./link_grib.csh '+self.WRF_DIR+'/DATA/fnl_')
            print('Running ungrib.exe')
            os.system('./ungrib.exe >& ungrib_data.log')
            print('Running metgrid.exe')
            os.system('./metgrid.exe >& log.metgrid')

            try:
                log_metgrid = open('log.metgrid')
                success_string = 'Successful completion of metgrid'
                if success_string in log_metgrid.readlines():
                    print('metgrid ended successfully!')
                else:
                    print('metgrid ended without success. Check log file')
                    sys.exit()
            except:
                print('metgrid did not generate log file')
                sys.exit()
        print('We went back to '+os.getcwd())


    def _change_WRF_namelist_input_file(self):

        fields = ['start_year', 'start_month', 'start_day', 'start_hour', 'end_year', 'end_month', 'end_day',
                  'end_hour', 'interval_seconds']
        values = [self.start_date, self.start_date, self.start_date, self.start_date, self.end_date, self.end_date,
                  self.end_date, self.end_date, self.interval_seconds]
        for f, v in zip(fields,values):
            self._replacefield(self.WRF_DIR + '/WRFV3/test/em_real/namelist.input', f, self._write_new_text_for_line_wrf(f, v))

    def run_WRF(self):
        if not os.path.exists(self.WORK_DIR + '/wps_out'):
            os.makedirs(self.WORK_DIR + '/wps_out')
        print('Starting WRF analysis. This might take a while')
        with working_directory(self.WRF_DIR+'/WRFV3/test/em_real'):
            print('Moving to ' + os.getcwd())
            os.system('ln -sf '+self.WRF_DIR+'/WPS/met_em* .')
            self._change_WRF_namelist_input_file()
            print('Running real.exe')
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

            print('Running wrf.exe')
            os.system('./wrf.exe')
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

    def clean_directories(self):
        with working_directory(self.WRF_DIR+'/WPS'):
            print('Cleaning WPS folder from output files')
            try:
                os.system('mv FILE* '+self.WORK_DIR+'/wps_out')
                os.system('mv geo_em.d* '+self.WORK_DIR+'/wps_out')
                os.system('mv met_em.d* ' + self.WORK_DIR + '/wps_out')

            except:
                print('There was a problem. Files were not created')
        with working_directory(self.WRF_DIR+'/WRFV3/test/em_real'):
            print('Cleaning WRFV3/test/em_real folder from output files')
            try:
                os.system('mv wrfinput_* ' + self.WORK_DIR + '/wrf_out')
                os.system('mv wrfout_* '+self.WORK_DIR+'/wrf_out')
                os.system('mv wrfbdy_* ' + self.WORK_DIR + '/wrf_out')
            except:
                print('There was a problem. Files were not created')
