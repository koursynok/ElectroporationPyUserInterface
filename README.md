# ElectroporationPyUserInterface
This code was written by David Gilardot, during his internship with the NBMS team at ENS de Chimie.  
If you access this code via a QRcode, remember to install all the necessary packages for a recent version of Python.  

Here we use IDLE (Python) 3.11.3 
In the cmd tool, run the commands below: 

pip install pyvisa 
pip install pyserial
pip install tk 
pip install time  

This repository cointain two different codes, OneChanel if you use a the device which use only one channel of the relay and TwoChannels for both. You can find a picture representing two differents device configuration. 

Note that when you run this code, the program will search for device connection :  
- To connect generator with GPIB, you have to download Keysight IO Library Suite and use IO Connection Expert to find your device the first time. Please let run the application at the start of your laptop to facilitate connection process for the following experiments.  
- GPIB configured on channel 16. Configure the GPIB correctly or modify line 17.
- RS485 modbus relay connected to your computer's USB 3 port. Choose the correct port or search in the device manager. To do this, open the manager, connect your USB/RS485 converter to the computer, search for it in the USB manager, open the device properties and note the slot number associated with this USB port. You can then change the COM port number used in the code on line 12.

If you don't want to connect to these devices when launching the code, modify lines 11 and 13, replacing 1 by 0 to bypass the device search. 

To use the user interface, a help file describes each part of the interface. Please download it and do not rename it so that it can be displayed directly in the interface. 
If you want to rename it, modify line 341 of the code. 

Thank you and enjoy with the electroporation device ;)
