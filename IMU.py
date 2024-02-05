


#Included the library files
import RPi.GPIO as GPIO
import smbus 
from time import sleep
import time
from random import randrange




#Not Used
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
INT_ENABLE   = 0x38
#Used
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F

Engine_Throttle_Actuator_position = 0
bus = smbus.SMBus(1) # or bus = smbus.SMBus(0) for older version boards

Device_Address = 0x68 # MPU6050 device address for I2C device

def Collective_Postioning(Data_Angle):
    Data_Angle = int(Data_Angle);time_diffrence = time.time()
    print(f"{Data_Angle} degrees",end = '')
    # Sample rate of 10 Hz = 10 times in 1 second. Diffrence in time is 0.1 for each output 
    print(f"\t Time stamp: {time_diffrence}")
    if Data_Angle >= 0 and Data_Angle <= 180:

        if Data_Angle < 5:
            Engine_Throttle_Actuator_position = 3

        elif Data_Angle >= 5 and Data_Angle < 15:
            Engine_Throttle_Actuator_position = 5

        elif Data_Angle >= 15 and Data_Angle < 45:
            Engine_Throttle_Actuator_position = linear_interpolation(Data_Angle)

        elif Data_Angle >= 45:
            Engine_Throttle_Actuator_position = 10
        
        else:
            Engine_Throttle_Actuator_position = 0
            print("Error! Value not between 0 and 10!")
            

    return Engine_Throttle_Actuator_position

def linear_interpolation(Data_Angle):
    Collective_Postioning_Solve = 5 + (Data_Angle - 15) * ((10 - 5)/ (45 - 15))

    return Collective_Postioning_Solve


def read_raw_data(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    Data_Angle = ((high << 8) | low)        
    if(Data_Angle > 32768):
            Data_Angle = Data_Angle - 65536
    return Data_Angle


def Generate_Data():
    value = randrange(180)
    return value



def Setup_Hardware():
    acc_x = read_raw_data(ACCEL_XOUT)
    acc_y = read_raw_data(ACCEL_YOUT)
    acc_z = read_raw_data(ACCEL_ZOUT)

    Ax = acc_x/16384.0
    Ay = acc_y/16384.0 
    Az = acc_z/16384.0


    in_min = 1
    in_max = -1
    out_min = 0
    out_max = 180
    angle = (Ay - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return angle

def setup(Hardware_Check):
    interval = 0.1; count=0 ;Data_Angle = 0
      
    while True:

        if Hardware_Check == True:
            Data_Angle=Setup_Hardware()
        else:
            Data_Angle=Generate_Data()  
         
        while True:

        
            start_time = time.time()
            Engine_Throttle = Collective_Postioning(Data_Angle)
            

            count+=1
            if(count >= 10):
                count = 0
                print("Engine Throttle Acutation position is:",end='')
                if(Engine_Throttle < 1 and Engine_Throttle > 0):
                    print(f"{Engine_Throttle} inch")
                else:
                    print(f"{Engine_Throttle} inches")


                print("\n")
                break

            time.sleep(max(0, interval - (time.time() - start_time)))



# Main calls
print("If you have a MPU6050 sensor module with Raspberry Pi board connected as declared in the Setup steps please Enter \"Yes\", Otherwise Enter \"No\" or press Enter: ",end='')
Hardware_Check = input()
Hardware_Check=Hardware_Check.lower()

if(Hardware_Check == 'yes'):
    Hardware_Check = True
else:
    Hardware_Check = False

Hardware_Check=bool(Hardware_Check)
setup(Hardware_Check)
        
        
        
"""
Question:
How would you verify the software against these requirements? What would your test steps, test inputs, and expected outputs be? Please elaborate on your decisions.
"""

""""
For understanding the expected outputs, it's essential to first comprehend the expected inputs. Begin by researching your expected inputs, then simulate these inputs through your software. You can generate data points and various elements to simulate data. When incorporating test steps, ensure that it works on simpler hardware or in Software in the Loop systems.

Simple ways of testing inputs:

* Connect to simple hardware to generate data.
* Based on research, automatically output all data points at a reasonable rate.
* Ways of testing outputs through software:

* Step through my functions for data capture from the sensor, ensuring that all aspects of the data look correct.
* Use PDB (Python Debugger) with an import of the functionalities.
* If tranfered to C GDB useage of Debugger 
* Least useful way: Print Statements.
* Utilization of a Serial Window Viewer.
* Usage of semihosting and OpenOCD for data inspection.
* Set breakpoints at each line with an integrated debugger.
* Print out registers and examine them accordingly.
* Design a framework to automatically test all outputs, including local, global, and various other data types.

Ways of testing outputs through hardware:
* Use a signal analyzer to ensure that voltages and outputs/inputs change as expected.
"""
