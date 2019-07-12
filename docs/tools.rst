.. _tools:

Tools
=====

grads2table.py
--------------

This is a program that allows the user to produce a table in txt format with the values that are produced by the wrf_analysis.py program.
It takes as inputs the ARWpost output files and can produce two distinct kind of file:

* Table with several parameter values for every date and pressure level in the input file for certain coordinates. The parameters fields that this table will contain are:
	* Date 
	* hour 
	* P 
	* T 
	* h 
	* 104dens 
	* U 
	* V 
	* wmr 
	* RH 
	* n 
	* year 
	* month 
	* day 
	* n/Ns 
	* wind_speed 
	* wind_direction 
	* MJD


* Table with several parameter values for the surface level at a certain coordinates

* Date 
* hour 
* T 
* RH 
* P 
* U 
* V 
* n 
* year 
* month 
* day 
* n/Ns 
* wind_speed 
* wind_direction 
* MJD

The surface level is determined by grads, taking into account the coordinates of interest and the geographycal information stored within the WRF package.

The program uses two grads scripts, located within the PYWRF_DIR/pyWRF/meteo_utils folder:

* cta_data5.gs, for pressure levels output
* cta_data6.gs, for surface output

The coordinates of interest are set by default to the MAGIC Telescopes location at the Observatorio de El Roque de los Muchachos, at the island of La Palma (Spain). However, the user can specify other coordinates of interest.

Here are some examples of usage of this program:

Example 1:

.. code-block:: bash

    > grads2table.py -f arwpost_filename.txt

This will create a table named arwpost_filename_final_table.txt containing the above mentioned fields.

Example 2:

.. code-block:: bash

    > grads2table.py -s -f arwpost_filename.txt

This will create a table with the surface level parameters, called arwpost_filename_final_surface_table.txt containig the above mentioned fields

Example 3: 

.. code-block:: bash

    > grads2table.py -m list_of_filenames.txt

This will merge the information from the files contained in that file. The list_of_filenames.txt file must have a filename per line.

.. code-block:: bash

    > grads2table.py -f arwpost_filename.txt -c 27.5 312.2

This will create the arwpost_filename_final_table.txt file but with the data corresponding to the coordinates specified with the -c flag. **The first value must be latitude and the second must be longitude, both in degrees**

.. code-block:: bash

    > grads2table.py -s -f arwpost_filename.txt -c 27.5 312.2

This will create the arwpost_filename_final_surface_table.txt file but with the data corresponding to the coordinates specified with the -c flag. **The first value must be latitude and the second must be longitude, both in degrees**



