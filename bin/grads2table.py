#!/usr/bin/env python

from pyWRF.meteo_utils.metorological_constants import *
import pandas as pd
import os
import argparse


def computedensity(p,T):
    return Ns * p / ps * Ts / T


def date2mjd(yyyy, mm, dd, hh, min=0, ss=0):
    """
    This function computes the mjd value corresponding to an input date, in the year, month, day, hour format

    Input:
        (integers) year, month, day and hour.
        Optionals: minutes and seconds. If left blank, they are assumed equal 0

    Output:
        (float) mjd
    """
    from astropy.time import Time
    y = str(int(yyyy))
    m = '{0:02}'.format(int(mm))
    d = '{0:02}'.format(int(dd))
    h = '{0:02}'.format(int(hh))
    mi = '{0:02}'.format(int(min))
    s = '{0:02}'.format(int(ss))
    t = Time(y + '-' + m + '-' + d + 'T' + h + ':' + mi + ':' + s, format='isot', scale='utc')
    return round(t.mjd, 2)


def compute_wind_direction(u,v):
    angle = np.arctan2(-1*u,-1*v)*180./np.pi
    if angle < 0.:
        angle += 360.
    direction = angle
    return direction


def compute_wind_speed(u,v):
    return np.sqrt(u**2. + v**2.)


def convert_grads_date_to_yyyymmdd(file_date):
    months = {'JAN':1, 'FEB':2, 'MAR':3,
          'APR':4, 'MAY':5, 'JUN':6,
          'JUL':7, 'AGO':8, 'SEP':9,
          'OCT':10, 'NOV':11, 'DEC':12}
    hour = file_date[:2]
    file_date = file_date[-9:]
    day = file_date[:2]
    month = file_date[2:5]
    year = file_date[5:]
    new_date = year+'{:02d}'.format(months[month])+day+' '+hour
    return new_date

# timestamp, P, T, h, 10^4n, u, v, wmr, RH


def read_grads_output(gradsout):
    with open(gradsout) as go:
        lines = go.readlines()
        line_to_print = []
        final_file = open(os.path.splitext(gradsout)[0]+'.txt', 'w')
        print('Date hour P T h 104dens U V wmr RH', file=final_file)
        for i, l in enumerate(lines):
            if len(l[:-1]) == 12:
                l = convert_grads_date_to_yyyymmdd(l[:-1])
                line_to_print.append(l)
                continue
            line_to_print.append(float(l[:-1]))
            if len(line_to_print) == 9:
                print(*line_to_print, file=final_file)
                line_to_print = []
        final_file.close()


def create_final_grads_table(intermediate_table, final_table):

    if os.path.exists(final_table):
        print('Output file %s already exists. Aborting.' % (final_table))
        sys.exit()
    else:
        read_grads_output(gradsout)
        intermediate_table = os.path.splitext(gradsout)[0]+'.txt'

    it = pd.read_csv(intermediate_table, sep=' ')
    #print('Date year month day hour MJD P Temp h n n/Ns U V wind_speed wind_direction RH', file=ft)
    it['n'] = computedensity(it['P'], it['T'])
    it['year'] = df['date'].apply(lambda x: str(x)[:4])
    it['month'] = df['date'].apply(lambda x: str(x)[4:6])
    it['day'] = df['date'].apply(lambda x: str(x)[6:8])
    it['MJD'] = date2mjd(it['year'], it['month'], it['day'], it['hour'])
    it['n/Ns'] = it['n']/Ns
    it['wind_speed'] = compute_wind_speed(it['U'], it['V'])
    it['wind_direction'] = compute_wind_direction(it['U'], it['V'])

    it.to_csv(final_table, sep=' ')

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


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', action='store_true', help='the grads output to convert to dataframe')
parser.add_argument('-m', '--merge', nargs='+', help='followed by a filename containing a list of txt files\n '
                                                     ' it merges them into a single txt file')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    if args.file:
        create_final_grads_table(args.file, os.path.splitext(args.file)[0]+'final_table.txt')
    elif args.merge:
        merge_txt_from_grib(args.file)
