import shortuuid
import random
import time


def get_random_drone_id():
    return shortuuid.ShortUUID().random(length=8)


def get_random_battery_level():
    return random.randrange(10, 100)


def get_drone_price():
    # drone price per minute
    # can be adjusted for different drone types if needed
    return 0.59


def get_random_closeby_position(position):
    # position e.g. {
    #   "lat": 48.14264857980008,
    #   "lng": 11.511508461819592
    # }
    position["lat"] += random.uniform(-0.0001, 0.0001)
    position["lng"] += random.uniform(-0.0001, 0.0001)
    return position


def get_current_time():
    """Get the current time in seconds.

    :return: Time in seconds (float).
             E.g.: 1702510907.4896383
    """
    return time.time()
