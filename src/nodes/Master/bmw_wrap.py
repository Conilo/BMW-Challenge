
import sys
sys.path.append("/home/pi/bmw/libs")

import time as tm
import boardIObk as bd
import motorbk as mt

# Initialize boarad objects
board = bd.boardbk()
board.Enable_Led(1)
board.Enable_Led(2)
board.Enable_Led(3)

# Initialize motor objects
left_motor = mt.motorbk(7)
right_motor = mt.motorbk(6)


def shutdown():
    """
    Function that takes care to properly
    close and clean GPIOs and motors.
    """
    left_motor.set(0)
    right_motor.set(0)
    board.CleanUp()
    print('GPIOs down')

def set_motors_speeds(vel_L, vel_R):
    """
    Funtion that sets the linear 
    velocities of both motors.
    """
    left_motor.set(vel_L)
    right_motor.set(vel_R)
    tm.sleep(0.1)
