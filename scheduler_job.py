from ntp import localtime
import uasyncio as asyncio
from scheduler import load_schedulers, get_schedules
from feeder import feed
from lcd_controller import lcd_write_line
import time

async def run_scheduled_jobs():
    """
    Continuously check the current time and execute feeding jobs
    based on the saved schedule.
    """
    while True:
        # Load the current schedules
        schedules = load_schedulers()
        
        # Display the next scheduled feeding time
        await display_next_schedule(schedules)
        
        # Get the current time in HH:MM format
        current_time_tuple = localtime()
        current_time = f"{current_time_tuple[3]:02}:{current_time_tuple[4]:02}"
        print(f"Current time: {current_time}")

        # Check if there's a job for the current time
        if current_time in schedules:
            size = schedules[current_time]
            print(f"Executing feeding job at {current_time} with size: {size}")

            # Map size to number of turns (example: small=3, medium=6, large=9)
            size_to_turns = {"small": 3, "medium": 6, "large": 9}
            turns = size_to_turns.get(size, 1)

            # Run the feeder
            await feed(turns)

            # Remove the executed schedule to prevent repeated execution
            del schedules[current_time]

        # Wait for 60 seconds before checking again
        await asyncio.sleep(30)

async def display_next_schedule(schedules):
    if schedules:
        next_time = min(schedules.keys())
        message = f"Next: {next_time}"
        print(message)
        await lcd_write_line(message, line=1)
    else:
        await lcd_write_line("No schedules", line=1)
