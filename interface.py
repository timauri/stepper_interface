import customtkinter
import serial 
import time
import json

comport = 'COM3'
ser = serial.Serial(comport, baudrate=9600, timeout=1)

def await_response(timeout=60):
    """awaits an input from the user"""
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
    """sends a command to the stepper motor"""
    ser.write((';'.join([command] + [str(a) for a in args]) + '\n').encode('utf-8'))

def validate(value):
    """converts input to an integer"""
    val = int(value)
    #print ({f'input value: {val} and type: {type(val)}'})
    return int(value)

app = customtkinter.CTk()
app.geometry = ('1000x1000')
app.title('Stepper Motor Interface')

def current_position():
    """ gets the current positional values of the motor and displays it"""
    current_angle = send_command('GET_ANGLE')
    ang_response = json.loads(await_response())
    angle = ang_response["result"]["angle"]
    current_step = send_command('GET_STEP_POS')
    step_out_response = json.loads(await_response())
    step_pos = step_out_response["result"]["step_pos"]

    frame_label.configure(
        text=f"Current Angle: {angle}°\nCurrent Absolute Step Position: {step_pos}"
    )

frame = customtkinter.CTkFrame(master=app, width=1500, height=1500)
frame.pack()

frame_label = customtkinter.CTkLabel(
    frame, text="Loading current position..."
)
frame_label.pack()

current_position()

stop_button = customtkinter.CTkButton(app, text="STOP MOTOR", 
                                      command=lambda: send_command('MOTOR_STOP'),
                                      fg_color='red')
stop_button.pack(padx=20, pady=20)

position_zero_button = customtkinter.CTkButton(app, text="SET MOTOR POSITION TO ZERO", 
                                               command=lambda: send_command('SET_POS_ZERO'),
                                               fg_color='blue')
position_zero_button.pack(padx=30)


#backward and forward buttons 
move_buttons_frame = customtkinter.CTkFrame(app)
move_buttons_frame.pack(pady=20)

forward_button = customtkinter.CTkButton(move_buttons_frame, text="Move 1\u00B0 forward", 
                                         command=lambda: send_command('MOVE_REL_ANGLE', 1, 'F'),
                                         fg_color='green', width=140)
forward_button.pack(side='left', padx = 10)
backward_button = customtkinter.CTkButton(move_buttons_frame, text="Move 1\u00B0 backward", 
                                          command=lambda: send_command('MOVE_REL_ANGLE', 1, 'B'),
                                          fg_color='green', width=140)
backward_button.pack(side='left', padx = 10)

#set angle buttons 
angle_var = customtkinter.StringVar()
set_angle_label = customtkinter.CTkLabel(app, text = 'Set Angle:')
set_angle_label.pack(pady = 10)
set_angle = customtkinter.CTkEntry(app, textvariable=angle_var)
set_angle.pack(pady = 10)

angle_buttons_frame = customtkinter.CTkFrame(app)
angle_buttons_frame.pack(pady=20)

rel_angle_button = customtkinter.CTkButton(angle_buttons_frame, text="Use relative angle", 
                                           command=lambda: send_command('MOVE_REL_ANGLE', validate(angle_var.get())))
abs_angle_button = customtkinter.CTkButton(angle_buttons_frame, text="Use absolute angle", 
                                           command=lambda: send_command('MOVE_ABS_ANGLE', validate(angle_var.get())))
rel_angle_button.pack(side='left', padx=10)
abs_angle_button.pack(side='left', padx=10)

app.mainloop()

