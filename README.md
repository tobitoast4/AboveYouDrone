# AboveYouDrone


Repository for AboveYouDrone Android app + mock python server. 
Use the app in combination with a DJI Ryze Tello drone and a ESP32 micro controller in the following setup:

<img src="doc\infrastructure_concept_new.png" width="600px"/>

Check out branch `tree/using_python_server` to test the app against the python mock server (found in `server/`). This python server is also running at [aboveyoudrone.pythonanywhere.com](https://aboveyoudrone.pythonanywhere.com/get_drones).

<img src="doc\infrastructure_concept.png" width="500px"/>

The following endpoints are implemented (yet the last two only in the python mock server):

| Endpoint path      | Description                                                                                                                                                                        |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| /get_drones        | Lists all drones including their positions. Can be used to display the drones on a map.                                                                                            |
| /rent_drone        | Sent when to renting a drone. Request body needs to contain the user id and the drone id. The rental succeeds if these values are valid and the drone is not being rented already. |
| /get_rental        | Gets the current active rental of a user based on their ID.                                                                                                                        |
| /stop_rental       | Ends an existing rental (if valid).                                                                                                                                                |
| /stop_drone_follow | Sends an instruction to the drone to stop following the current renter.                                                                                                            |
| /drone_follow      | Sends an instruction to the drone to resume following.                                                                                                                             |
| /panic_button      | Sends an instruction to start an alarm for instance.                                                                                                                               |
| /take_snapshot     | Takes a snapshot for the _IdentificationActivity_.                                                                                                                                   |
| /confirm_snapshot  | Confirms the snapshot for the _IdentificationActivity_.         