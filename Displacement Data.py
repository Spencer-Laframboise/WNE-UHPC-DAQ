from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
import pandas as pd
import datetime
import nidaqmx

#  function that will save the data as a csv file
def save_data():

    global x_data, y_data

    #  converts the x values into a more readable time format
    time_values = []
    for term in x_data:

        #  changes the value into a more readable format
        value = str(mdates.num2date(term)).split(" ")[-1]

        #  attempts to clean it up more
        #new_value = value.split('+')[0]

        time_values.append(value)

    #  uses the first point as the zero point
    intercept = -10.45 * y_data[0]

    #  converts the y values from voltage to displacement
    displacement_values = []
    for term in y_data:

        #  calculates new value
        new_value = round(10.45*term + intercept, 3)

        #  adds the new value to the list
        displacement_values.append(new_value)
    
    # Create a DataFrame from the data
    df = pd.DataFrame({'Time': time_values, 'Displacement (mm)': displacement_values})

    #  makes sure that the user selects a save file
    while True:

        # Save DataFrame to CSV using asksaveasfilename instead of asksaveasfile
        path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                        title="Save CSV File as ....",
                                        filetypes=[("CSV files", "*.csv")])
        
        #  confirms the user did not cancel
        if path:

            df.to_csv(path, index=False)
            print(f"Data saved to {path}")
            break

# Function to collect and update data
def collect_data():
    global state, x_data, y_data, line, ax, canvas, task, after_id

    #  stops updating if state is false
    if not state:
        return

    #  collects the x and y data values
    current_time = datetime.datetime.now()
    value = round(task.read(), 2)

    #  adds them to the appropriate lists
    x_data.append(mdates.date2num(current_time))
    y_data.append(value)

    #  updates the plot
    line.set_xdata(x_data)
    line.set_ydata(y_data)

    #  updates the plot view
    ax.relim()
    ax.autoscale_view()
    canvas.draw()

    #  schedules the next update with timing for 5 data points per second
    after_id = win.after(165, collect_data)

#  function to start or stop the program
def change_state():
    global state, win, after_id, task

    if not state:

        #  starts the data collection process
        state = True
        collect_data()

    else:

        #  saves the data from the experiment
        state = False
        save_data()

        #  cancels any ungoing tasks
        if after_id:
            win.after_cancel(after_id)

        #  closes everything
        task.close()
        win.quit()
        win.destroy()

# Initialize state, data lists, after_id, and task
state = False
x_data, y_data = [], []

#  loops to make sure the device is connected
while True:
    try:
        task = nidaqmx.Task()
        task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
        break
    except:
        messagebox.showerror("Error", "Make sure to connect a device then click okay")
        
after_id = None

# Create Tkinter window
win = tk.Tk()
win.geometry('650x550')
win.title('Data Collection')

# Start and stop buttons
start = tk.Button(win, text='Start', font=('Arial', 18), command=change_state)
start.grid(row=0, column=0)

stop = tk.Button(win, text='Stop', font=('Arial', 18), command=change_state)
stop.grid(row=0, column=1)

# Setup the plot
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data, 'b-')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
ax.set_xlabel('Time (HH:MM:SS)')
ax.set_ylabel('Value from sensor')

# Embed the plot in Tkinter
canvas = FigureCanvasTkAgg(fig, master=win)
canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, sticky=tk.W + tk.E)
canvas.draw()

# Pack the frame and run Tkinter
win.mainloop()