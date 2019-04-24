.. _setup:

Setup
=====

The steps you need to do are:

* Install and compile WRF
* Install or check for installation of needed Python libraries
* Install pyWRF

Install and compile WRF
-----------------------

The most difficult part is to have the WRF package properly installed and compiled.
There is a `tutorial <http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php>`__
to install and compile with certain level of warranty, but it does not always goes well.

Once you have the WRF package compiled and running you can continue installing the pyWRF package.

Install or check for installation of needed Python libraries
------------------------------------------------------------

The additional needed Python libraries that pyWRF needs to run properly are:

* os
* sys
* configparser
* glob
* datetime
* contextlib

You can install them either by using `pip <https://pypi.org/project/pip/>`__ or `conda <https://docs.conda.io/en/latest/>`__, depending on your Python installation. In order to install the missing library (sys, in the next example) you can install it by typing:

.. code-block:: bash

    pip install sys 

or

.. code-block:: bash

    conda install sys 

Once you have all the needed Python libraries you can proceed to install pyWRF.

Install pyWRF
-------------

You can get the pyWRF package from the GitHub repository. In order to download it, just type:

.. code-block:: bash

    git clone https://github.com/pmunar/pyWRF

Once downloaded, put the pyWRF folder in the directory where you want to 
install it (if you downloaded it elsewhere):

.. code-block:: bash

    > mv pyWRF /path/where/you/want/to/install/it

With the package in place, cd to the pyWRF directory:

.. code-block:: bash

    > cd pyWRF

and install it with the pip command:

.. code-block:: bash

    > pip install .

Note the "." at the end of the order. It is important!

Once installed (it takes a few seconds) it is almost ready to run.

Before running, the init-pywrf.sh script must be executed. It sets some
usefull and important environment variables. But before running this script
there are two changes that need to be done in it:

1- change the PYWRF_DIR value to the path where you installed pyWRF:

.. code-block:: bash

    > export PYWRF_DIR=/example/path/pyWRF

2- change the WRF_DIR value to the path where you installed and compiled
   the WRF software:

.. code-block:: bash

    > export WRF_DIR=/example/path/WRF

Once it is done, the script can be executed:

.. code-block:: bash

    > ./init-pywrf.sh

This script must be executed every time that the pyWRF package wants to be
used. An easy solution is to make an alias and put it into the .bashrc file.
An example of the line that would go into the .bashrc file:

.. code-block:: bash

    alias init-pywrf=". /path/where/you/installed/it/pyWRF/init-pywrf.sh"

After that, before using the software, type:

.. code-block:: bash

    > init-pywrf

from wherever directory and the package will be ready.