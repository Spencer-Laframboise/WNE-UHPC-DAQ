#  DAQ Connection Project
##  Introduction
This program was developed to allow for the user to collect displacement data from a sensor and save the data as a csv file. Data is collected at a rate of 5 points a second. There is a user interface with a start and stop button as well as a graph that shows the progress of the data collection over time. This is used by the WNE UHPC team for one of their tests.

## Required Modules
This program requires tkinter, matplotlib, pandas, datetime, and the national instruments python module nidaqmx. These can be installed by running this command in your terminal:

    pip install -r requirements.txt

##  Driver Requirements
If LabVIEW has not been installed on your system you will need to install National Instrument's driver for the DAQ. This will allow your device to register the connection and allow the program to read the values. The driver can be installed by clicking [this link](https://www.ni.com/en/support/downloads/drivers/download.ni-device-drivers.html?srsltid=AfmBOoph9_NydRDV9iTYhFOHP_ZvaTP0ea5yqzod91VWArIghLcADGAp#327643). Please note that this driver is Windows only.

##  Hardware Setup
###  Materials Used
- Linear Potentiometer:
    - [Click here to purchase](https://www.hgsind.com/product/lpps-sl-series-linear-potentiometer-position-sensor-spring-loaded?srsltid=AfmBOoqRE5v-Uud2FOCeDpvcn0W5e-HI-Pue0Ld3n4PBeCedTIWjSXhb&v=223)
    - This version was created specifically for the 2 inch version (LPPS-SL-050)
    -  This device measures the displacement of the rod and turns it into a change in voltage 

- National Instruments USB DAQ:
    - [Click here to purchase](https://www.ni.com/en/shop/data-acquisition/entry-level-usb-daq.html)
    - Use to collect the data from the potentiometer
###  Sensor Wiring
The [datasheet](https://www.hgsind.com/sites/default/files/2024-08/LPPS-SL%20Spring%20Loaded%20Linear%20Potentiometer_Data%20Sheet_Rev15.pdf) for the potentiometer includes this diagram for the wiring of the sensor:

![Sensor Setup](./Wiring%20Pinout.png)

To connect the sensor to the DAQ wire the blue wire to a GND pin, the brown wire to the 5V pin, and the black wire to the A2 analog pin. This can be done using a breadboard or with a direct connection.

###  Conversions
I could not find a conversion factor in the datasheet so to convert the change in voltage to a change in displacement I used some linear interpolation. To find the slope of the line for the conversion equation I found the average voltage outputs and corresponding distances. On each occurance of the code running a new intercept is created using the first point of data collection as the zero point, making the displacement as the spring expands positive.

##  Python Files in the Repository
###  Displacement Data.py
This is the completed code, allowing for the user to connect their DAQ to their computer and to collect data from the sensor. Once the collection is done pressing the stop button will cause a file dialog to pop up and allow the user to create a file path for the csv to be saved to. There is also an exe file for this python code.

###  Displacement Data Test.py
This is a file to test the user interface of the program, using random data as y values the graph will populate and when stopped can be saved to a csv file.

###  connection_test.py
This is a test to make sure that the DAQ is connected properly, this terminal based solution can be used to debug any issues

