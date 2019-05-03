import datetime
import os
import sys
from pyWRF.utils import working_directory
from pyWRF import environ


class RunAnalysis:
    """
    Analysis of global assimilation system data (GDAS, GFS, ECMWF, ...) with the WRF analysis software

    Attributes:
        group_start_date: datetime.datetime object representing the initial date of the analysis
        group_end_date: datetime.datetime object representing the final date of the analysis
        path_to_input_data: absolute path where the input data is located. The input data may be GDAS, GFS or ECMWF data
        path_to_output_data: absolute path where the final output files may be stored
        server: string representing the global data assimilation system of the input data. Default value: "GDAS".
                Other possible values are: "GFS" or "ECMWF"
        hour_step: integer representing the time difference, in hours, of the successive data input files and outputs.

    """

    def __init__(self,group_start_date, group_end_date, path_do_input_data, path_to_output_data, data_format,
                 num_domains, hour_step, server, parallel, ncores):

        self.start_date = group_start_date   # datetime object format
        self.end_date = group_end_date       # datetime object format
        self.analysis_interval = self.end_date - self.start_date
        self.input_data_dir = path_do_input_data
        self.output = path_to_output_data
        self.run_hours = self.analysis_interval.total_seconds() // 3600 + hour_step
        self.hour_step = hour_step
        self.interval_seconds = int(self.hour_step * 3600.)
        self.server = server
        self.data_format = data_format
        self.num_domains = num_domains
        self.parallel = parallel
        self.ncores = ncores

        self.WRF_DIR = environ.DIRS.get('WRF_DIR')
        self.WORK_DIR = self.input_data_dir

    def _write_new_text_for_line_wps(self, field, value):
        """
        Returns a new line for the wps nameilst.wps file changing the 'field' parameter according to the 'value'
        parameter

        :param field: string representing the field of the file that will be changed
        :param value: datetime.datetime object or integer or float
        :return: new_line (String)
        """

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
        """
        Returns a new line for the wps nameilst.wps file changing the 'field' parameter according to the 'value'
        parameter

        :param field: string representing the field of the file that will be changed
        :param value: datetime.datetime object or integer or float
        :return: field_to_write. String. New line corresponding to the field and its new value
        """
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
        """
        Returns the original file with the searchExp value replaced by replaceExp

        :param file: string representing the file where to search for the 'searchExp' value
        :param searchExp: string that will be searched within the file
        :param replaceExp: string that will replace the searchExp parameter in the file
        :return:
        """
        import fileinput
        for line in fileinput.FileInput(file, inplace=1):
            if searchExp in line:
                line = line.replace(line, replaceExp)
            sys.stdout.write(line)

    def _change_WPS_namelist_input_file(self):
        """
        :return: Returns the namelist.wps file with the 'start_date', 'end_date' and 'interval_seconds' fields replaced by the
        ones according to the start_date, end_date and interval_seconds that are input to the class
        """
        fields = ['start_date', 'end_date', 'interval_seconds']
        values = [self.start_date, self.end_date, self.interval_seconds]
        for f, v in zip(fields, values):
            self._replacefield(self.WRF_DIR + '/WPS/namelist.wps', f, self._write_new_text_for_line_wps(f, v))

    def _link_input_data_to_WPS(self):
        """
        :return: Function to make a sym link of the output files of the WPS folder into the $WRF_DIR/DATA folder, that
        will be input for the WRF processing
        """
        from pyWRF.utils import datetime_to_filename_format
        date = self.start_date
        while date <= self.end_date:
            date_filename_format = datetime_to_filename_format(date)
            infile = 'fnl_%s.%s'%(date_filename_format, self.data_format)
            if not os.path.islink(self.WRF_DIR+'/DATA/'+infile):
                os.system('ln -s '+self.input_data_dir+'/'+infile+' '+self.WRF_DIR+'/DATA')
            date += datetime.timedelta(hours=self.hour_step)

    def _link_vtables(self):
        """
        :return: Function to make a sym link of the Vtables corresponding to the input data files.
        """
        if self.server == 'GDAS' or self.server == 'GFS':
            vtable = 'Vtable.GFS'
        elif self.server == 'ERA-Interim' or self.server == 'ECMWF':
            vtable = 'Vtable.ECMWF'
        cwd = os.getcwd()
        os.system('ln -sf '+cwd+'/ungrib/Variable_Tables/'+vtable+' '+cwd+'/Vtable')

    def run_wps(self):
        """
        Function that runs the PREPROCESSING algorithms geogrid.exe, ungrib.exe and metgrid.exe
        """
        self._change_WPS_namelist_input_file()
        self._link_input_data_to_WPS()

        print('=========================================================')
        print('Starting PREPROCESSING. This might take a while')
        print('=========================================================')
        if not os.path.exists(self.output + '/wps_out'):
            os.makedirs(self.output + '/wps_out')

        with working_directory(self.WRF_DIR+'/WPS'):
            print('We moved to '+os.getcwd())
            print('Running geogrid.exe')
            os.system('./geogrid.exe >& log.geogrid')
            try:
                log_geogrid = open('./log.geogrid')
                success_string = '!  Successful completion of geogrid.        !\n'
                if success_string in log_geogrid.readlines():
                    print('Geodrid ended successfully!')
                else:
                    print('Geogrid ended without success. Check log file')
                    sys.exit()
            except:
                print('Geogrid did not generate log file')

            self._link_vtables()
            os.system('./link_grib.csh '+self.WRF_DIR+'/DATA/fnl_')
            print('Running ungrib.exe')
            os.system('./ungrib.exe >& ungrib_data.log')
            print('Running metgrid.exe')
            os.system('./metgrid.exe >& log.metgrid')

            try:
                log_metgrid = open('./log.metgrid')
                success_string = '!  Successful completion of metgrid.  !\n'
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
        """
        :return: returns the namelis.input file for WRF processing changed according to the fields 'start_year',
        'start_month', 'start_day', 'start_hour', 'end_year', 'end_month', 'end_day', 'end_hour', 'interval_seconds'
        that are taken from the input parameters of the RunAnalysis Class.
        """

        fields = ['start_year', 'start_month', 'start_day', 'start_hour', 'end_year', 'end_month', 'end_day',
                  'end_hour', 'interval_seconds']
        values = [self.start_date, self.start_date, self.start_date, self.start_date, self.end_date, self.end_date,
                  self.end_date, self.end_date, self.interval_seconds]
        for f, v in zip(fields,values):
            self._replacefield(self.WRF_DIR + '/WRFV3/test/em_real/namelist.input', f, self._write_new_text_for_line_wrf(f, v))

    def run_WRF(self):
        """
        Function that runs the PROCESSING of the WRF program, by running real.exe and wrf.exe programs.
        """
        if not os.path.exists(self.output + '/wrf_out'):
            os.makedirs(self.output + '/wrf_out')
        print('=========================================================')
        print('Starting WRF analysis. This might take a while')
        print('=========================================================')
        with working_directory(self.WRF_DIR+'/WRFV3/test/em_real'):
            print('Moving to ' + os.getcwd())
            os.system('ln -sf '+self.WRF_DIR+'/WPS/met_em* .')
            self._change_WRF_namelist_input_file()
            print('Running real.exe')
            if self.parallel:
                os.system('mpirun -np {} ./real.exe'.format(str(self.ncores)))
            else:
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
            if self.parallel:
                os.system('mpirun -np {} ./wrf.exe'.format(str(self.ncores)))
            else:
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

    def _write_new_text_for_line_arwpost(self, field, value, domain):
        """
        Returns a new line for the wps nameilst.ARWpost file changing the 'field' parameter according to the 'value'
        parameter

        :param field: string representing the field of the file that will be changed
        :param value: datetime.datetime object or integer or float
        :return: new_line (String)
        """

        if type(value) == datetime.datetime:
            year = value.year
            month = value.month
            day = value.day
            hour = value.hour
            date_to_write = '{:d}-{:02d}-{:02d}_{:02d}:00:00'.format(year, month, day, hour)
            date_field = date_to_write + "','" + date_to_write + "','" + date_to_write
            if field == 'start_date' or field == 'end_date':
                new_line = ' ' + field + " = '" + date_field + "',\n"
            elif field == 'input_root_name' or field == 'output_root_name':
                new_line = ' ' + field + " = './wrfout_d0"+str(domain)+"_" + date_field + "',\n"
            return new_line
        elif type(value) == int or type(value) == float:
            new_line = ' ' + field + " = " + str(value) + ',\n'
            return new_line

    def _change_ARWpost_namelist_input_file(self, ndom):
        """
        :return: Returns the namelist.ARWpost file with the 'start_date', 'end_date', 'interval_seconds' and name roots
        fields replaced by the ones according to the start_date, end_date and interval_seconds that are input to the
        class
        """
        fields = ['start_date', 'end_date', 'interval_seconds', 'input_root_name', 'output_root_name']
        values = [self.start_date, self.end_date, self.interval_seconds, self.start_date, self.end_date]
        for f, v in zip(fields, values):
            self._replacefield(self.WRF_DIR + '/ARWpost/namelist.ARWpost', f,
                               self._write_new_text_for_line_arwpost(f, v, ndom))

    def run_ARWpost(self):
        """
        Function that runs the POSTPROCESSING of the WRF program, by running GRADS program.
        """

        if not os.path.exists(self.output + '/arwpost_out'):
            os.makedirs(self.output + '/arwpost_out')
        print('=========================================================')
        print('Starting ARWpost analysis. This might take a while')
        print('=========================================================')
        with working_directory(self.WRF_DIR + '/ARWpost'):
            print('Moving to ' + os.getcwd())
            os.system('ln -sf ' + self.WRF_DIR + '/WRFV3/test/em_real/wrfout_* '+os.getcwd())
            for ndom in range(1, self.num_domains +1):
                self._change_ARWpost_namelist_input_file(ndom)
                print('Running ARWpost.exe for domain 0%s'%(ndom))
                os.system('./ARWpost.exe')

    def clean_directories(self):
        """
        Function that moves the output files created by run_wps and run_wrf functions into the output directory
        specified by the user in the config file, in the output_path field.
        """
        with working_directory(self.WRF_DIR+'/WPS'):
            print('Cleaning WPS folder from output files')
            try:
                os.system('mv FILE* '+self.output+'/wps_out')
                os.system('mv geo_em.d* '+self.output+'/wps_out')
                os.system('mv met_em.d* ' + self.output + '/wps_out')

            except:
                print('There was a problem. Files were not created')
        with working_directory(self.WRF_DIR+'/WRFV3/test/em_real'):
            print('Cleaning WRFV3/test/em_real folder from output files')
            try:
                os.system('mv wrfinput_* ' + self.output + '/wrf_out')
                os.system('mv wrfout_* '+self.output+'/wrf_out')
                os.system('mv wrfbdy_* ' + self.output + '/wrf_out')
            except:
                print('There was a problem. Files were not created')

        with working_directory(self.WRF_DIR + '/ARWpost'):
            print('Cleaning ARWpost folder from output files')
            try:
                os.system('mv wrfout_*dat ' + self.output + '/arwpost_out')
                os.system('mv wrfout_*ctl ' + self.output + '/arwpost_out')
            except:
                print('There was a problem. Files were not created')


