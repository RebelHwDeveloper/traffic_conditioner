.. Traffic Conditioner documentation master file, created by
   sphinx-quickstart on Tue Nov  5 07:59:21 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Configuration of Project Environment
*************************************

This is the traffic conditioner project for Linux devices.

Overview on How to Run this API
================================
1. Either install the package via the pip command or launch in standalone mode via the launcher
2. Install packages required

Setup procedure
===============
1. Configure system path
    A. You need root privileges::

            sudo su

      .. note:: In my case, I had to change both of system paths. This may not be necessary

    B. Add the module to the PYTHONPATH
        - Add the directory to the python3 system search path::

            export PYTHONPATH=$PYTHONPATH:/path/you/want/to/add

2. Install Dependencies
    - Install requirements::

            pip3 install -r requirements.txt

3. Run tests
    A. Use the `unittest` module::

            python3 -m unittest -v test.test_generic

    B. Either run the line below
        $ python3 test/test_generic.py

4. Run app.py::

    python3 launcher.py

5. Refer to Traffic Controller how to test the code through iperf3

