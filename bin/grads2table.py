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


def create_final_grads_table(gradsout, final_table):

    if os.path.exists(final_table):
        print('Output file %s already exists. Aborting.' % (final_table))
        sys.exit()
    else:
        read_grads_output(gradsout)
        intermediate_table = os.path.splitext(gradsout)[0]+'.txt'

    it = pd.read_csv(intermediate_table, sep=' ')
    #print('Date year month day hour MJD P Temp h n n/Ns U V wind_speed wind_direction RH', file=ft)
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

def modify_grads_script(input_file, grads_script):
    with open(grads_script, 'r') as gs:
        gst = open(grads_script+'.temp', 'w')
        lines = gs.readlines()
        new_lines = []
        for l in lines:
            new_lines.append(l[:-1])
        lines = new_lines
        lines[0] = lines[0].split(' ')[0] + ' '+ os.path.splitext(input_file)[0]+"'"
        lines[13] = lines[13].split('(')[0] + "('" + os.path.splitext(input_file)[0] + ".txt'," + lines[13].split(',')[1]
        ll = [26, 29, 32, 35, 38, 41, 44, 47]
        for l in ll:
            lines[l] = lines[l].split('(')[0] + "('" + os.path.splitext(input_file)[0] + ".txt'," + lines[l].split(',')[1] + ',append)'
        for l in lines:
            print(l, file=gst)
        gst.close()

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', help='the grads output to convert to dataframe')
parser.add_argument('-m', '--merge', help='followed by a filename containing a list of txt files\n '
                                                     ' it merges them into a single txt file')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    if args.file:
        print('the file to process is:', args.file)
        modify_grads_script(args.file, 'cta_data5.gs')
        os.system('grads -bpcx cta_data5.gs.temp')
        create_final_grads_table(args.file, os.path.splitext(args.file)[0]+'final_table.txt')
    elif args.merge:
        merge_txt_from_grib(args.merge)
