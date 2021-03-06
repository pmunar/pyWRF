#!/usr/bin/env python

from pyWRF.meteo_utils.metorological_constants import *
import pandas as pd
import os
import argparse
import sys
import numpy as np


def computedensity(p,T):
    return Ns * p / ps * Ts / T


def date2mjd(df):
    """
    This function computes the mjd value corresponding to an input date, in the year, month, day, hour format

    Input: dataframe

    Output:
        (float) mjd
    """
    from astropy.time import Time
    df['MJD'] = df.apply(lambda x: Time(str(x['year']) + '-' + str(x['month']) + '-' + str(x['day']) +
                            ' {0:02}'.format(x['hour'])+':00:00').mjd, axis=1)

    return df


def compute_wind_direction(u,v):
    angle = np.arctan2(-1*u,-1*v)*180./np.pi
    angle[angle < 0] +=360
    direction = angle
    return direction


def compute_wind_speed(u,v):
    return np.sqrt(u**2. + v**2.)


def convert_grads_date_to_yyyymmdd(file_date):
    months = {'JAN':1, 'FEB':2, 'MAR':3,
          'APR':4, 'MAY':5, 'JUN':6,
          'JUL':7, 'AUG':8, 'SEP':9,
          'OCT':10, 'NOV':11, 'DEC':12}
    hour = file_date[:2]
    file_date = file_date[-9:]
    day = file_date[:2]
    month = file_date[2:5]
    year = file_date[5:]
    new_date = year+'{:02d}'.format(months[month])+day+' '+hour
    return new_date


def read_grads_output(gradsout, lenout=9):
    with open(gradsout) as go:
        lines = go.readlines()
        line_to_print = []
        final_file = open(os.path.splitext(gradsout)[0]+'.txt', 'w')
        if lenout == 9:
            print('Date hour P T h 104dens U V wmr RH', file=final_file)
        elif lenout == 7:
            print('Date hour T RH P U V', file=final_file)
        for i, l in enumerate(lines):
            if len(l[:-1]) == 12:
                l = convert_grads_date_to_yyyymmdd(l[:-1])
                line_to_print.append(l)
                continue
            line_to_print.append(float(l[:-1]))
            if len(line_to_print) == lenout:
                print(*line_to_print, file=final_file)
                line_to_print = []
        final_file.close()


def create_final_grads_table(gradsout, final_table):

    if os.path.exists(final_table):
        print('Output file %s already exists. Aborting.' % (final_table))
        sys.exit()
    else:
        read_grads_output(gradsout, lenout=9)
        intermediate_table = os.path.splitext(gradsout)[0]+'.txt'

    it = pd.read_csv(intermediate_table, sep=' ')
    it['n'] = computedensity(it['P']/100., it['T'])
    it['year'] = it['Date'].apply(lambda x: str(x)[:4])
    it['month'] = it['Date'].apply(lambda x: str(x)[4:6])
    it['day'] = it['Date'].apply(lambda x: str(x)[6:8])
    it['n/Ns'] = it['n']/Ns
    it['wind_speed'] = compute_wind_speed(it['U'], it['V'])
    it['wind_direction'] = compute_wind_direction(it['U'], it['V'])
    it = date2mjd(it)
    it.sort_values(by=['MJD','P'], inplace=True)
    it['P'] = it['P'].round(1) / 100.
    it.to_csv(final_table, sep=' ', index=False)
    os.remove(os.path.splitext(gradsout)[0]+'.txt')


def create_surface_grads_table(gradsout, final_table):

    if os.path.exists(final_table):
        print('Output file %s already exists. Aborting.' % (final_table))
        sys.exit()
    else:
        read_grads_output(gradsout, lenout=7)
        intermediate_table = os.path.splitext(gradsout)[0]+'.txt'

    it = pd.read_csv(intermediate_table, sep=' ')
    it['n'] = computedensity(it['P']/100., it['T'])
    it['year'] = it['Date'].apply(lambda x: str(x)[:4])
    it['month'] = it['Date'].apply(lambda x: str(x)[4:6])
    it['day'] = it['Date'].apply(lambda x: str(x)[6:8])
    it['n/Ns'] = it['n']/Ns
    it['wind_speed'] = compute_wind_speed(it['U'], it['V'])
    it['wind_direction'] = compute_wind_direction(it['U'], it['V'])
    it = date2mjd(it)
    it.sort_values(by=['MJD','P'], inplace=True)
    it['P'] = it['P'].round(1)
    it.to_csv(final_table, sep=' ', index=False)


def merge_txt_from_grib(txtfile, output_file='merged_from_single_grads_outputs.txt'):
    lf = open(txtfile, 'r')
    outfile = open(output_file, 'w')

    line = lf.readline()
    first = True
    while line:
        datafile = open(line[:-1], 'r')
        if first:
            dataline = datafile.readline()
        else:
            datafile.readline()
            dataline = datafile.readline()

        while dataline:
            print(dataline[:-1], file=outfile)
            dataline = datafile.readline()
        first = False
        datafile.close()
        line = lf.readline()
    lf.close()
    outfile.close()


def modify_grads_script(input_file, grads_script, lat=28.76, lon=342.12):
    infile = os.path.splitext(input_file)[0]
    with open(grads_script, 'r') as gs:
        gst = open(os.getcwd()+'/'+grads_script.split('/')[-1]+'.temp', 'w')
        print(os.getcwd()+'/'+grads_script.split('/')[-1])
        lines = gs.readlines()
        new_lines = []
        for l in lines:
            new_lines.append(l[:-1])
        lines = new_lines
        lines[0] = lines[0].split(' ')[0] + ' ' + infile + "'"
        lines[5] = lines[5].split('=')[0] + "='" + infile + ".txt'"
        lines[1] = lines[1].split('lat')[0] + 'lat ' + str(lat) +"'"
        lines[2] = lines[2].split('lon')[0] + 'lon ' + str(lon) + "'"
        for l in lines:
            print(l, file=gst)
        gst.close()

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='the grads output to convert to dataframe')
parser.add_argument('-m', '--merge', help='followed by a filename containing a list of txt files\n'
                                          ' it merges them into a single txt file')
parser.add_argument('-s', '--surface', action='store_true', help='creates the table for surface values')
parser.add_argument('-c', '--coordinates', nargs='+', help='lat and lon coordinates of the place of interest, \n '
                                                'in degrees')

if __name__ == "__main__":
    args = parser.parse_args()
    if args.file:
        print('the file to process is:', args.file)
        if args.surface:
            if args.coordinates:
                lat, lon = args.coordinates
                modify_grads_script(args.file, os.environ['PYWRF_DIR']+'/pyWRF/meteo_utils/cta_data6.gs',
                                    lat=lat, lon=lon)
            else:
                modify_grads_script(args.file, os.environ['PYWRF_DIR'] + '/pyWRF/meteo_utils/cta_data6.gs')
            os.system('grads -bpcx cta_data6.gs.temp')
            create_surface_grads_table(args.file, os.path.splitext(args.file)[0]+'final_surface_table.txt')
            os.remove('cta_data6.gs.temp')
        else:
            if args.coordinates:
                lat, lon = args.coordinates
                modify_grads_script(args.file, os.environ['PYWRF_DIR'] + '/pyWRF/meteo_utils/cta_data5.gs',
                                    lat=lat, lon=lon)
            else:
                modify_grads_script(args.file, os.environ['PYWRF_DIR']+'/pyWRF/meteo_utils/cta_data5.gs')
            os.system('grads -bpcx cta_data5.gs.temp')
            create_final_grads_table(args.file, os.path.splitext(args.file)[0]+'final_table.txt')
            os.remove('cta_data5.gs.temp')
    elif args.merge:
        merge_txt_from_grib(args.merge)
