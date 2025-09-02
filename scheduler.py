import json

SCHEDULER_FILE = "scheduler.json"
FOOD_SIZES = ["small", "medium", "large"]

def load_schedulers():
    try:
        with open(SCHEDULER_FILE, "r") as f:
            return json.load(f)
    except OSError:
        return {}

def save_schedulers(schedulers):
    with open(SCHEDULER_FILE, "w") as f:
        json.dump(schedulers, f)
    # No recursion or undefined variables
    return schedulers

def get_schedules():
    return load_schedulers()

def add_schedule(time_str, size):
    assert size in FOOD_SIZES, "Invalid food size"
    schedulers = load_schedulers()
    schedulers[time_str] = size
    save_schedulers(schedulers)
    return schedulers

def update_schedule(time_str, size):
    schedulers = load_schedulers()
    if time_str not in schedulers:
        raise KeyError("Schedule time not found")
    if size is not None:
        assert size in FOOD_SIZES, "Invalid food size"
        schedulers[time_str] = size
    save_schedulers(schedulers)
    return schedulers

def delete_schedule(time_str):
    schedulers = load_schedulers()
    if time_str not in schedulers:
        raise KeyError("Schedule time not found")
    del schedulers[time_str]
    save_schedulers(schedulers)
    return schedulers
