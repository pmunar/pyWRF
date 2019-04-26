# init-pywrf.sh sets some environment variables for pyWRF.
#
# One way is to put this e.g. in ~/.bashrc or ~/.profile:
#
# export PYWRF_DIR=< location of your pyWRF software checkout >
# alias init_pyWRF="source $PYWRF_DIR/init-pywrf.sh"
#
# This way your python, PATH, PYTHONPATH, ... is not set to the
# pyWRF software when you log in to your system, yet you can
# conveniently set up your shell for pyWRF by executing the aliases:
# $ init_pyWRF

export WRF_WPS_DIR=$WRF_DIR/WPS
export WRF_WRFV3_DIR=$WRF_DIR/WRFV3
export WRF_ARWpost_DIR=$WRF_DIR/ARWpost

export PATH=$PATH:$PYWRF_DIR:$PYWRF_DIR/bin:$PYWRF_DIR/pyWRF
export PYTHONPATH=$PYWRF_DIR:$PYWRF_DIR/bin:$PYWRF_DIR/pyWRF:$PYTHONPATH