import random
import utils

drones = []
# list of entries:
# {
#     "id": <STR>,
#     "price": <FLOAT>,  # price per minute
#     "user_id": <STR>,  # the one who is currently renting the drone (None if nobody is renting it)
#     "timestamp_rental_started": <FLOAT>  unix timestamp
# }
drones_positions = []
# list of entries:
# {
#     "id": <STR>,
#     "battery": <INT>,
#     "price": <FLOAT>,
#     "position": <DICT>
# }


def get_drone_by_id(drone_id):
    for drone in drones:
        if drone["id"] == drone_id:
            return drone
    return None


def get_drone_by_user_id(user_id):
    for drone in drones:
        if drone["user_id"] == user_id:
            return drone
    return None


def create_drones():
    positions = [
        {
            "lat": 48.1423415209611,
            "lng": 11.511997110488098
        },
        {
            "lat": 48.09165769491002,
            "lng": 11.644732285917598
        }
    ]
    for position in positions:
        create_drones_in_area(position)


def create_drones_in_area(position):
    # position e.g. {
    #   "lat": 48.14264857980008,
    #   "lng": 11.511508461819592
    # }
    amount_of_drones = random.randrange(3, 7)
    for _ in range(amount_of_drones):
        drone_id = utils.get_random_drone_id()
        drones.append({
            "id": drone_id,
            "price": utils.get_drone_price(),
            "user_id": None,
            "timestamp_rental_started": None
        })
        drones_positions.append({
            "id": drone_id,
            "battery": utils.get_random_battery_level(),
            "price": utils.get_drone_price(),
            "position": utils.get_random_closeby_position(position.copy())
        })
