from src.drone_controller.input_layer.drone_state import DroneState
from src.drone_controller.input_layer.drone_state_mapper import DroneStateMapper


def test_keyboard_simple_up():
    position = [0, 0, 3]
    velocity = [0, 0, 3]
    velocity_ang = [0, 0, 0]
    acceleration = [0, 0, 3]
    acceleration_ang = [0, 0, 0]

    expected_state = DroneState(position, velocity, velocity_ang, acceleration, acceleration_ang)

    position = [0, 0, 0]
    velocity = [0, 0, 0]
    acceleration = [0, 0, 0]
    drone_state = DroneState(position, velocity, velocity_ang, acceleration, acceleration_ang)

    user_input = {"Rotation Forward": 0,
                  'Rotation Right': 0,
                  "Rotation Backward": 0,
                  "Rotation Left": 0,
                  "Acceleration": 3}

    mapper = DroneStateMapper()
    future_state: DroneState = mapper.keyboard(drone_state, user_input)

    assert future_state == expected_state
