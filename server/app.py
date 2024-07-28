import math
import time

from flask import Flask, request
from flask import send_file
import os

import drone
import utils

app = Flask(__name__)


app.secret_key = "secret key"
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

drone.create_drones()


@app.route('/')
def home():
    api_info = {
        "API": "AboveYouDrone",
        "VERSION": 1.0,
        "DATE": "2024-05-31"
    }
    return api_info


@app.route('/get_drones', methods=['GET'])
def get_drones():
    return {
        "drones": drone.drones_positions
    }


@app.route('/rent_drone', methods=['POST'])
def rent_drone():
    """Body should look like:
    {
        user_id: <uuid>,
        drone_id: <uuid>
    }
    """
    user_id = request.values.get("user_id")
    the_drone = drone.get_drone_by_user_id(user_id)
    if the_drone is not None:  # it should be none, otherwise, the user is already renting a drone
        return {
            "status": "error",
            "message": "You are already renting a drone"
        }
    drone_id = request.values.get("drone_id")
    the_drone = drone.get_drone_by_id(drone_id)
    if the_drone["user_id"] is not None:
        return {
            "status": "error",
            "message": "This drone is already being rented"
        }
    else:
        current_timestamp = utils.get_current_time()
        the_drone["user_id"] = user_id
        the_drone["timestamp_rental_started"] = current_timestamp
        return {
            "status": "success",
            "user_id": user_id,
            "drone_id": drone_id,
            "timestamp_rental_started": current_timestamp
        }


@app.route('/get_rental', methods=['POST'])
def get_rental():
    """Body should look like:
    {
        user_id: <uuid>
    }
    """
    user_id = request.values.get("user_id")
    the_drone = drone.get_drone_by_user_id(user_id)
    if the_drone is None:
        return {
            "active_rental": "no",
        }
    return {
        "active_rental": "yes",
        "user_id": user_id,
        "drone_id": the_drone["id"],
        "timestamp_rental_started": the_drone["timestamp_rental_started"]
    }


@app.route('/stop_rental', methods=['POST'])
def stop_rental():
    """Body should look like:
    {
        user_id: <uuid>,
        drone_id: <uuid>
    }
    """
    user_id = request.values.get("user_id")
    drone_id = request.values.get("drone_id")
    the_drone = drone.get_drone_by_user_id(user_id)
    if the_drone is None or the_drone["id"] != drone_id:
        return {
            "status": "error",
            "message": "Drone not found"
        }
    else:
        timestamp_rental_started = the_drone["timestamp_rental_started"]
        current_timestamp = utils.get_current_time()
        time_of_rental = current_timestamp - timestamp_rental_started
        price_to_pay = time_of_rental / 60 * the_drone["price"]
        price_to_pay = round(price_to_pay, 2)

        the_drone["user_id"] = None  # set back the current rental (so that the drone has no active rental)
        the_drone["timestamp_rental_started"] = None

        return {
            "status": "success",
            "user_id": user_id,
            "drone_id": the_drone["id"],
            "timestamp_rental_started": timestamp_rental_started,
            "timestamp_rental_ended": current_timestamp,
            "price_to_pay": price_to_pay
        }


@app.route('/drone_follow', methods=['POST'])
def drone_follow():
    """Body should look like:
    {
        user_id: <uuid>,
        drone_id: <uuid>
    }
    """
    user_id = request.values.get("user_id")
    drone_id = request.values.get("drone_id")
    the_drone = drone.get_drone_by_user_id(user_id)
    if the_drone is None or the_drone["id"] != drone_id:
        return {
            "status": "error",
            "message": "Wrong drone id"
        }
    else:
        # TODO @Leo: Send command
        return {
            "status": "success",
            "message": "Drone will continue following"
        }


@app.route('/stop_drone_follow', methods=['POST'])
def stop_drone_follow():
    """Body should look like:
    {
        user_id: <uuid>,
        drone_id: <uuid>
    }
    """
    user_id = request.values.get("user_id")
    drone_id = request.values.get("drone_id")
    the_drone = drone.get_drone_by_user_id(user_id)
    if the_drone is None or the_drone["id"] != drone_id:
        return {
            "status": "error",
            "message": "Wrong drone id"
        }
    else:
        # TODO @Leo: Send command
        return {
            "status": "success",
            "message": "Following will be stopped"
        }


@app.route('/take_snapshot', methods=['POST'])
def take_snapshot():
    """Body should look like:
    {
        user_id: <uuid>,
        drone_id: <uuid>
    }
    """
    user_id = request.values.get("user_id")
    drone_id = request.values.get("drone_id")
    the_drone = drone.get_drone_by_user_id(user_id)
    if the_drone is None or the_drone["id"] != drone_id:
        return {
            "status": "Error: Wrong drone id"
        }
    else:
        # TODO @Leo: Get image from drone
        filename = 'test_image.png'
        return send_file(filename, mimetype='image/png')
        # return {
        #     "user_id": user_id,
        #     "drone_id": the_drone["id"],
        #     "image": None,      # TODO: Send image
        #     "image_hash": None  # TODO: Generate and send image hash
        # }


@app.route('/confirm_snapshot', methods=['POST'])
def confirm_snapshot():
    """Body should look like:
    {
        user_id: <uuid>,
        image_hash: <str>
    }
    """
    user_id = request.values.get("user_id")
    image_hash = request.values.get("image_hash")
    # TODO @Leo: Use the taken image as basis for person identification
    # TODO: check image hash
    the_drone = drone.get_drone_by_user_id(user_id)
    if the_drone is None:
        return {
            "status": "error",
            "message": "Drone not found"
        }
    else:
        return {
            "user_id": user_id,
            "drone_id": the_drone["id"],
            "status": "success"
        }

# TODO: Implement panic button


if __name__ == '__main__':
    app.run("0.0.0.0", port=int(os.environ.get("PORT", 80)), debug=False, threaded=True, processes=1)