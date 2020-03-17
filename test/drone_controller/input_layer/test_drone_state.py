from src.drone_controller.input_layer.drone_state import DroneState


def test_create_three_dimensional_position():
    """
    Test dict generation for a three dimensional position.
    """
    position = [1, 1, 1]
    velocity = [1, 1, 1]
    velocity_ang = [1, 1, 1]
    acceleration = [1, 1, 1]
    acceleration_ang = [1, 1, 1]
    drone_state = DroneState.create(position, velocity, velocity_ang, acceleration, acceleration_ang)

    expected_dict = {
        "Position": position,
        "Velocity": velocity,
        "Angular Velocity": velocity_ang,
        "Acceleration": acceleration,
        "Angular Acceleration": acceleration_ang
    }

    state_dict = drone_state.state

    assert state_dict == expected_dict
