import os

WRF_DIR = os.environ.get('WRF_DIR', '')
WRF_DATA = os.environ.get('WRF_DATA', '')
WRF_WPS = os.environ.get('WRF_WPS', '')
WRF_WRFV3 = os.environ.get('WRF_WRFV3', '')
WRF_ARWpost = os.environ.get('WRF_ARWpost', '')

DIRS = {
    'WRF_DIR' : WRF_DIR,
    'WRF_DATA': WRF_DATA_DIR,
    'WRF_WPS' : WRF_WPS_DIR,
    'WRF_WRFV3' : WRF_WRFV3_DIR,
    'WRF_ARWpost' : WRF_ARWpost_DIR
}