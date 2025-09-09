import uasyncio as asyncio
from scheduler import load_schedulers
from feeder import feed
import time

async def run_scheduled_jobs():
    """
    Continuously check the current time and execute feeding jobs
    based on the saved schedule.
    """
    while True:
        # Load the current schedules
        schedules = load_schedulers()
        
        # Get the current time in HH:MM format
        current_time_tuple = time.localtime()
        current_time = f"{current_time_tuple[3]:02}:{current_time_tuple[4]:02}"

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
        await asyncio.sleep(60)

# Entry point for the scheduler job
# Removed the main function and its invocation
