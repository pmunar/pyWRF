import glob
import os


def gunzip_and_rename_files(path, format):
    """
    Function that performs the decompression of the input files, if they are still in gzip format. If they are already
    decompressed, it does nothing
    :param path: string
    :return:
    """
    try:
        print('Decompressing all data files in this folder')
        print('Changing all file names. The original name is kept cut after grib2')
        for i, filename in enumerate(glob.glob(path + '/*.*')):
            if filename.lower().endswith('.gz'):
                os.system('gunzip '+filename)
                new_filename = filename.split(format)[0]+ format
            else:
                new_filename = filename.split(format)[0] + format
            os.rename(filename, new_filename)
    except:
        print('There are no files to decompress or rename. Exiting')


