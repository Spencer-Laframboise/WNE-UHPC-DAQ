from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
import pandas as pd
import datetime

#  function that will save the data as a csv file
def save_data():

    #  need to reformat the time value in x data
    global x_data, y_data

    #  converts the x values into a more readable time format
    time_values = []
    for term in x_data:
        time_values.append(mdates.num2date(term))

    #  converts the y values from voltage to displacement
    displacement_values = []
    for term in y_data:
        displacement_values.append(term)
    
    # Create a DataFrame from the data
    df = pd.DataFrame({'Time': time_values, 'Value': displacement_values})

    # Save DataFrame to CSV
    path = filedialog.asksaveasfile(mode='w', defaultextension=".csv", title="Save CSV File as ....")
    df.to_csv(path, index=False)

    print("Data saved to data.csv")

# Function to collect and update data
def collect_data():
    global state, x_data, y_data, line, ax, canvas, after_id

    if not state:
        return  # Stop updating if state is False

    current_time = datetime.datetime.now()
    value = len(x_data)  # Simulating data increase

    x_data.append(mdates.date2num(current_time))
    y_data.append(value)

    line.set_xdata(x_data)
    line.set_ydata(y_data)

    ax.relim()
    ax.autoscale_view()
    canvas.draw()

    # Store the after ID
    after_id = win.after(100, collect_data)  

# Function to start/stop data collection
def change_state():
    global state, win, after_id

    if not state:
        state = True
        collect_data()  # Start updating data
    else:
        state = False
        save_data()
        if after_id:
            win.after_cancel(after_id)  # Cancel using the stored ID
        win.quit()  # Quit the mainloop
        win.destroy()  # Destroy the window

# Initialize state and data lists
state = False
x_data, y_data = [], []
after_id = None  # Add global after_id variable

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

# Embed the plot in Tkinter
canvas = FigureCanvasTkAgg(fig, master=win)
canvas.get_tk_widget().grid(row=2, column=0, columnspan=2, sticky=tk.W + tk.E)
canvas.draw()

# Pack the frame and run Tkinter
win.mainloop()