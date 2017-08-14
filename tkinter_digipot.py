import Tkinter
from Tkinter import Tk, Label, Button, Canvas, Entry
import sys
import time
import RPi.GPIO as GPIO

SPI_CS_PIN = 8
SPI_SDI_PIN = 10 # mosi
SPI_SDO_PIN = 22 # miso
SPI_CLK_PIN = 11

GPIO.setwarnings(False)

# define GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPI_CS_PIN, GPIO.OUT)
GPIO.setup(SPI_CLK_PIN, GPIO.OUT)
GPIO.setup(SPI_SDI_PIN, GPIO.OUT)
GPIO.setup(SPI_SDO_PIN, GPIO.IN)

###
#Declare mypoti class to and initialize tkinter master 
###
class MyPoti(Tkinter.Tk):
    def __init__(self, master):
        Tkinter.Tk.__init__(self,master)
        self.master = master
        self.initialize()

    def initialize(self):
		#create canvas with specified size and add 
        w = Canvas(self, width=700, height=600)
        w.pack()
	
		#Declare two lists, one for front labels, anthoer for answer labels
        self.flabels = []
        self.alabels = []
		#Define x and y cordinates for lables
        self.flblx = 280
        self.flbly = 40
        self.alblx = 380
        self.albly = 40

		#Dummy list
        self.my_list = []
	
		#Text to set on front lables
        self.str_label = ['POTI0', 'POTI1','POTI2','POTI3','POTI4']
	
		#Trigger to check if we want to program or pause
        self.running = True
        
		#Define environment varibales for input text fields
		#We can change/update this during runtime
        self.entry_pot_var = Tkinter.StringVar()
        self.entry_res_var = Tkinter.StringVar()
		
		#Define text areas for input onr for poti selection and one for resistence value
        self.entry_pot = Entry(self,textvariable=self.entry_pot_var, validate="focusout")
        self.entry_res = Entry(self,textvariable=self.entry_res_var, validate="focusout")

		#Initial text to display on above text fields
        self.entry_pot_var.set("Enter Pot selection")
        self.entry_res_var.set("Enter resistor value - 2000 to 100000") 

		#Set pot selection entry as highlighted
        self.entry_pot.selection_range(0,Tkinter.END)
        #self.entry_res.selection_range(0,Tkinter.END)

		#Set keyboard focus on pot text field
        self.entry_pot.focus_set()

		#Add pot text field to canvas
        self.entry_pot.pack()
		
		#ToDO
		#validate input for pot selection
        #self.entry_pot["validatecommand"] = (self.register(self.check_pot), "%P")
		
		#Add resistence text field to canvas
        self.entry_res.pack()
        
		#Create two text on the canvas with x and y coodrinates
        w.create_window(120, 40, window=self.entry_pot)
        w.create_window(120, 70,window=self.entry_res)

		#We declare 5 front lables and add them to canvas with x and y co ordinates
        for x in range(5):
            print self.str_label[x]
            self.label = Label(self, text=self.str_label[x], fg='white', bg='black')
            self.label.pack()
            self.flabels.append(self.label)

		#We declare 5 answer lables and add them to canvas with x and y co ordinates
        for x in range(5):
            self.label = Label(self, text='values', fg='white', bg='blue')
            self.label.pack()
            self.alabels.append(self.label)

		#Create front label in canvas
        for label in self.flabels:
            w.create_window(self.flblx,self.flbly,window=label)
            self.flbly = self.flbly + 19

		#Create answer label in cavas
        for label in self.alabels:
            w.create_window(self.alblx,self.albly,window=label)
            self.albly = self.albly + 20

		###
		#Button definitions
		###
		#Start button, and add callback to start_app function when this button is clicked
        self.start_button = Button(self, text="Set", height=2, width=10, command=self.start_app)
        self.start_button.pack()

		#Clear button, and add callback to clear_app function when this button is clicked
        self.clear_button = Button(self, text="Clear", height=2, width=10, command=self.clear_app, state="disabled")
        self.clear_button.pack()

		#Clear button, and add quit function of tkinter master when this button is clicked
        self.close_button = Button(self, text="Close", height=2, width=10, command=self.quit)
        self.close_button.pack()

        #Add buttons to canvas
        w.create_window(70, 170, window=self.start_button)
        w.create_window(190, 170, window=self.close_button)
        w.create_window(310, 170, window=self.clear_button)
	
	#Input validation for pot selection text field
    def check_pot(self, txt):
        print("POT validate!")
        #pot = self.entry_pot_var.get()
        if int(txt):
            if txt < 0 or txt > 4 :
                return False
            else:
                return True
        else:
            print("Not integer")
            self.entry_pot.focus_set()
            self.entry_pot.delete(0, END)

            return False
	#Input validation for resistence text field
    def check_res(self):
        print("Greetings!")

    def start_app(self):
        """ 
        Start the application when start button pressed
        """
        #Disable start button after presed
        global running
        self.running = True
        #self.start_button.config(state="disabled")
        self.clear_button.config(state="normal")
        print "Starting app!"
		#call update values function
        self.update_values()

    def clear_app(self):
        """
        Clear the answer lable fields 
        """
        print "Clear"
        global running
        self.running = False
        self.start_button.config(state="normal")
        self.clear_button.config(state="disabled")
        for i in range(5):
            self.alabels[i].config(text=str("values"))
		
		#Clear the text fields and set default vaule
        self.entry_pot_var.set("Enter Pot selection")
        self.entry_res_var.set("Enter resistor value - 2000 to 100000")
		
		#set keyboard focus
        self.entry_pot.focus_set()

    def stop_app(self):
        """
        Stop the app
        """
        print "Stopping"
        self.quit()

    def update_values(self):
        """
        Helper function to trigger label values after reading pot and res values
        """
        #if self.running:
        #    self.after(1000, self.update_values)

		#Read input value given for pot selection text field
        pot = self.entry_pot.get()
        #if pot < 0 or pot > 4 :
		
		#Read input value given for  resistence text field
        res = self.entry_res.get()
		
		#call update text value function which converts values and send data to MCP
        self.update_text_values(pot, res)

    def update_text_values(self, pot, res):
        """
        Update the answer lables values with resistence
        """
        #resisitor to data conversion
        byte = 256
        local_pot = 100000
        local_res = 125
        #rw = int(res) * 1000
        #rw = int(rw) - int(local_res)
        #lev = float((rw * byte) / local_pot)
        #level =round(lev)
        #level = int(level)
        #level = int(res) - int(local_res)
        if float(res):
            level = float(res) - int(local_res)
        else:
            level = int(res) - int(local_res)
        level = (level * byte) / local_pot
		level = int(level)
        print(level)
        b = 0

        if int(pot) == 0:
            b = "0001" "0001" "{0:08b}".format(level)
        if int(pot) == 1:
            b = "0001" "0001" "{0:08b}" '{0:016b}'.format(level)
        if int(pot) == 2:
            b = "0001" "0001" "{0:08b}" '{0:032b}'.format(level)
        if int(pot) == 3:
            b = "0001" "0001" "{0:08b}" '{0:048b}'.format(level)
        if int(pot) == 4:
            b = "0001" "0001" "{0:08b}" '{0:064b}'.format(level)

        print b 
		#update answer label based on poti selection
        self.alabels[int(pot)].config(text=str(level))
		
        for x in b:
            GPIO.output(SPI_SDI_PIN, int(x))
            print(int(x))
            GPIO.output(SPI_CLK_PIN, True)
            GPIO.output(SPI_CLK_PIN, False)
            GPIO.output(SPI_CS_PIN, True)
        self.update_idletasks()

if __name__ == "__main__":
    #root.geometry("400x250")
    mypoti = MyPoti(None)
    mypoti.title("DIGI POTI")
    mypoti.mainloop()
