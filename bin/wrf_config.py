#!/usr/bin/env python
import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('config', help='The name of the configuration file')
args = parser.parse_args()

if not os.path.exists('./'+args.config):
    os.system('cp $PYWRF_DIR/config_file/config_example.conf ' + args.config)
else:
    answer = input('The configuration file exists in current path.\n Do you want to overwrite it? [y/n]: ')
    if answer == 'y':
        os.system('cp $PYWRF_DIR/config_file/config_example.conf ' + args.config)
    elif answer == 'n' or answer != 'y':
        sys.exit()