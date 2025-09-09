# Feeder module to control 28BYJ-48 stepper motor using GP2-GP5
# Assumes MicroPython environment with machine.Pin

from lcd_controller import lcd_write_line
from machine import Pin
from stepper_28byj48 import Stepper28BYJ48
import uasyncio as asyncio

# Setup pins GP2-GP5 for IN1-IN4
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
IN3 = Pin(4, Pin.OUT)
IN4 = Pin(5, Pin.OUT)


# Create stepper instance
stepper = Stepper28BYJ48(IN1, IN2, IN3, IN4)  # ~0.244ms per step for 4096 steps in 1s

# Add a state variable to track motor activity
motor_running = False

async def feed(turns = 1):
    """
    Run the stepper motor for a given number of full rotations.
    If the motor is already running, stop it instead.
    """
    global motor_running
    
    await lcd_write_line("Feeding...", line=1)
    if motor_running:
        # Stop the motor if it's already running
        await stop()
        motor_running = False
    else:
        # Start the motor
        motor_running = True
        await stepper.run(turns, 1)
        await stepper.release()
        motor_running = False
        
    await lcd_write_line("READY", line=1)

async def stop():
    """
    Stop the current feeding operation.
    """
    await stepper.stop()

    await lcd_write_line("READY", line=1)
