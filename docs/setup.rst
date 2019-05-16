.. _setup:

Setup
=====

The steps you need to do are:

* Install and compile WRF
* Install or check for a Python installation in your system
* Install or check for installation of needed Python libraries
* Install pyWRF

Install and compile WRF
-----------------------

The most difficult part is to have the WRF package properly installed and compiled.
There is a `tutorial <http://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php>`__
to install and compile with certain level of warranty, but it does not always go well.

Once you have the WRF package compiled and running you can continue installing the pyWRF package.


Install or check for a Python installation in your system
---------------------------------------------------------

If you are using Linux, it is probable that you already have a Python installation ready in your system. However, I recommend you to make a parallel installation using `Anaconda <https://www.anaconda.com/>`__ distribution. This is an open-source Python distribution which allows the user to easily install packages in a clean and transparent way.

I will assume you have this distribution installed from now on. For other ways to install Python and associated packages, there is a lot of information around in the net.

Install or check for installation of needed Python libraries
------------------------------------------------------------

The additional needed Python libraries that pyWRF needs to run properly are:

* os
* sys
* configparser
* glob
* datetime
* contextlib
* argparse

You can install them either by using `pip <https://pypi.org/project/pip/>`__ or `conda <https://docs.conda.io/en/latest/>`__, depending on your Python installation. In order to install the missing library (sys, in the next example) you can install it by typing:

.. code-block:: bash

    pip install sys 

or

.. code-block:: bash

    conda install sys 

Once you have all the needed Python libraries you can proceed to install pyWRF.

Parallel execution
------------------

If you plan on running your analysis in parallel with more than one CPU, you should also install the OpenMPI library. For instance, in Ubuntu you can do it by typing in your terminal:

.. code-block:: bash

    > sudo apt-get install openmpi-bin openmpi-common openssh-client openssh-server libopenmpi1.3 libopenmpi-dbg libopenmpi-dev

For installation in other operative systems, please referr to the `OpenMPI website <https://www.open-mpi.org/>`__.


Install pyWRF
-------------

You can get the pyWRF package from the GitHub repository. In order to download it, just type:

.. code-block:: bash

    > git clone https://github.com/pmunar/pyWRF

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
there are two environment variables that need to be set:

1- export the PYWRF_DIR variable. You can do it from the terminal:

.. code-block:: bash

    > export PYWRF_DIR=/example/path/pyWRF

2- export the WRF_DIR. You can do it from the terminal:

.. code-block:: bash

    > export WRF_DIR=/example/path/WRF

For making the process more confortable for you, we recommend you to put these two exports within your .bashrc file.

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