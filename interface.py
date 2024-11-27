import customtkinter
import serial 
import time


#update with actual COM port once I know
comport = 'COM7'
#ser = serial.Serial(comport, baudrate=9600, timeout=1)

#holds different arguments for each command 
arguments_dict = {
    'MOVE_REL_STEPS': ['steps', 'direction', [int, str]],
    'MOVE_REL_ANGLE': ['angle', [float]],
    'MOVE_CONTINUOUS': ['direction', [str]],
    'MOVE_ABS_ANGLE': ['angle', [float]],
    'MOVE_ABS_STEPS': ['step_pos', [int]],
    'SET_POS_ZERO': [],
    'GET_ANGLE': [],
    'GET_STEP_POS': []
}

"""
def await_response(timeout=60):
   awaits an input from the user
    reply = None
    t0 = time.time()
    while True:
        while ser.in_waiting > 0:
            reply = ser.readline().decode().strip()  # Read and decode reply
        else:
            if reply != None:
                return reply
        time.sleep(0.1)
        if time.time() - t0 > timeout:
            return None

def send_command(command, *args):
    sends a command to the stepper motor
    ser.write((';'.join([command] + [str(a) for a in args]) + '\n').encode('utf-8'))
"""

app = customtkinter.CTk()
app.geometry = ('500x500')
app.title('Stepper Motor Interface')

step_var = customtkinter.StringVar()
dir_var = customtkinter.StringVar()
angle_var = customtkinter.StringVar()
step_pos_var = customtkinter.StringVar()

def send_command(command, *args):
    """empty function for testing"""
    pass 

def optionmenu_callback(choice):
    """ defines what happens when a specific argument is chosen from the dropdown"""
    if choice == 'SET_POS_ZERO' or choice == 'GET_ANGLE' or choice == 'GET_STEP_POS':
        send_command(choice)
        print (f'Sending command {choice} to stepper motor')
    elif choice == 'MOVE_REL_ANGLE' or choice == 'MOVE_ABS_ANGLE':
        angle = angle_var.get()
        send_command(choice, angle)
        print (f'Sending command {choice} to stepper motor')
    elif choice == 'MOVE_REL_STEPS':
        steps = step_var.get()
        direction = dir_var.get()
        send_command(choice, steps, direction)
    elif choice == 'MOVE_CONTINUOUS': 
        send_command(choice, direction)
        print (f'Sending command {choice} to stepper motor')
    else:
        step_pos = step_pos_var.get()
        send_command(choice, step_pos)               
    
    
    """
    if choice == 'MOVE_REL_STEPS':
        send_command('MOVE_REL_STEPS', steps, direction)
        print(f'Sending command {choice} to stepper motor')
    elif choice == 'MOVE_REL_ANGLE':
        send_command('MOVE_REL_ANGLE', angle)
        print(f'Sending command {choice} to stepper motor')
    else:
        send_command('MOVE_ABS_ANGLE', angle)
        print(f'Sending command {choice} to stepper motor')
    """



#command choices 
optionmenu = customtkinter.CTkOptionMenu(app, values=["MOVE_REL_STEPS", 
                                                      "MOVE_REL_ANGLE",
                                                      "MOVE_CONTINUOUS",
                                                      "MOVE_ABS_ANGLE",
                                                      "MOVE_ABS_STEPS",
                                                      "SET_POS_ZERO",
                                                      "GET_ANGLE",
                                                      "GET_STEP_POS"],
                                         command=optionmenu_callback)
optionmenu.set("Choose an option")
optionmenu.grid(padx = 20, pady = 20, sticky = 'ew')


# arguments display - need to have boxes stretch to display all text
steps_entry = customtkinter.CTkEntry(app, textvariable=step_var)
steps_label = customtkinter.CTkLabel(app, text = 'Steps')
steps_label.grid(row = 1, column = 0)
steps_entry.grid(row = 1, column = 1, sticky = 'ew')

direction_entry = customtkinter.CTkEntry(app, textvariable=dir_var)
direction_label = customtkinter.CTkLabel(app, text = 'Direction')
direction_label.grid(row = 2, column = 0, ipadx = 20)
direction_entry.grid(row = 2, column = 1, sticky = 'ew')

angle_entry = customtkinter.CTkEntry(app, textvariable=angle_var)
angle_label = customtkinter.CTkLabel(app, text = 'Angle')
angle_label.grid(row = 3, column = 0)
angle_entry.grid(row = 3, column = 1, sticky = 'ew')

step_pos_entry = customtkinter.CTkEntry(app, textvariable=step_pos_var)
step_pos_label = customtkinter.CTkLabel(app, text = 'Step Position')
step_pos_label.grid(row = 4, column = 0)
step_pos_entry.grid(row = 4, column = 1, sticky = 'ew')

button = customtkinter.CTkButton(app, text="Enter")
button.grid(padx = 10, pady = 10)


app.mainloop()

"""
things to consider:
- when telling it to move to a certain angle, won't move to actual angle unless it's a multiple of 180 degrees (move-rel-angle/move-abs-angle)
- read in argument values from user 
- check type of input to make sure only valid inputs are made
- need an enter button 
- want to show options after drop down option is selected 
"""

