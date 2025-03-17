#  need to add the ability to create a table with timestamp and data
import nidaqmx
import time

#  the connection name from the computer (found in the NI MAX)
connection_name = "Dev1"

#  analog pin for the displacement device (found on the physical DAQ)
analog_pin = "ai2"

#  creates a connection with the DAQ
with nidaqmx.Task() as task:

    #  adding a channel for the device
    task.ai_channels.add_ai_voltage_chan("{}/{}".format(connection_name, analog_pin))

    #  reading the value from the daq
    values = []
    for _ in range(100):

        #  reads the data from the DAQ
        value = task.read()
        values.append(value)
        print("Value: {}".format(value))
        time.sleep(0.2)

    task.close()

    print("Average Value = {}".format(sum(values)/len(values)))