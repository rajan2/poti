import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from Tkinter import *
import time
import Adafruit_MCP3008

#Define running trigger to start/pause
running = True
#List to store values
my_list = []
# Front lables to display
flabels = []
# Answer lables
alabels = []

#initialize MCP

# Software SPI configuration:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} |'.format(*range(4)))
print('-' * 65)

def start_app():
    """
    Start the application when start button pressed
    """
    global running
    running = True
    #Disable start button after presee
    start_button.config(state=DISABLED)
    pause_button.config(state=NORMAL)
    print "Starting app!"
    update_values()

def pause_app():
    """ 
    Pause
    """
    print "Pausing "
    global running
    running = False
    start_button.config(state=NORMAL)
    pause_button.config(state=DISABLED)

def stop_app():
    """
    Stop the app
    """
    stop_button.config()
    print "Stopping"
    master.quit()

def update_values():
    """
    Helper function to trigger label values after reading list
    """
    my_list = read_adc_values()
    update_label_values(my_list)
    # Repeat the function after 1s (no need time.sleep)
    if running:
        master.after(1000, update_values)

def read_adc_values():
    """
    Return values from adc
    """
    # Read all the ADC channel values in a list.
    values = [0]*5
    volt = [0]*5
    curr = [0]*5
    resis = [0]*5
    v = 4.980
    bit = 1023
    for i in range(5):
        # The read_adc function will get the value of the specified channel (0-7).
        values[i] = (mcp.read_adc(i) * v / bit)
        volt = values[:]
        values[i] = v - values[i]
        curr[i] = values[i] / 11000
        resis[i] = volt[i] / curr[i]
        if volt[i] == 0:
            continue
        else:
            volt[i] = volt[i]
        resis[i] = resis[i] / 1000
        resis[i] = round(resis[i], 2)
        # Print the ADC values.
    print('| {0:>4} KOhm | {1:>4} KOhm | {2:>4} KOhm | {3:>4} KOhm | {4:>4} KOhm |'.format(*resis))
    return resis

def update_label_values(my_list):
    """
    Update the answer lables values with list
    """
    for j in range(5):
        alabels[j].config(text=str(my_list[j])+' KOhm')
    master.update_idletasks()

#Declare new master
master = Tk()

#Create a canvas to place label and button at desired place
w = Canvas(master, width=400, height=300)
w.pack()

#Example string
string = 'Channel'

#Define x axis for front label
lblx = 70

#Define Y axis for front label
lbly = 50

#Loop over and define labels Here i need 5 labels
for x in range(5):
    str_label = string + str(x)
    label = Label(master, text=str_label, fg='white', bg='black')
    label.pack()
    flabels.append(label)
    
#Add Front lables to canvas
for label in flabels:
    w.create_window(lblx,lbly,window=label)
    lbly = lbly + 20

#Define x axis for answer label
lblx = 140

#Define y axis for answer label
lbly = 50

#Loop over and define labels Here i need 5 labels
for x in range(5):
    str_label = string + str(x)
    label = Label(master, text=str_label, fg='white', bg='blue')
    label.pack()
    alabels.append(label)

#Add Answer lables to canvas    
for label in alabels:
    w.create_window(lblx,lbly,window=label)
    lbly = lbly + 20

#Create start button and call start_app function
start_button = Button(master, text="Start",height=2, width=10, command=start_app)
start_button.pack()

#Create pause button and call pause_app function
pause_button = Button(master, text="Pause",height=2, width=10, command=pause_app)
pause_button.pack()

#Create Stop button to exit program
stop_button = Button(master, text="Stop",height=2, width=10, command=stop_app)
stop_button.pack()

#Add buttons to canvas
w.create_window(70, 170, window=start_button)
w.create_window(190, 170, window=stop_button)
w.create_window(310, 170, window=pause_button)

#main loop
master.mainloop()
