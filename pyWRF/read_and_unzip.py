import glob
import os


def gunzip_and_rename_files(path):
    """
    Function that performs the decompression of the input files, if they are still in gzip format. If they are already
    decompressed, it does nothing
    :param path: string
    :return:
    """
    try:
        print('Decompressing all data files in this folder')
        print('Changing all file names. The original name is kept cut after grib2')
        for i, filename in enumerate(glob.glob(path + '/*.gz')):
            os.system('gunzip '+filename)
            filename = filename.split('.gz')[0]
            new_filename = filename.split('grib2')[0]+'grib2'
            os.rename(filename, new_filename)
    except:
        print('There are no files to decompress or rename. Exiting')


