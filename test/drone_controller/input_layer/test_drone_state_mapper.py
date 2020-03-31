from unittest import TestCase

from src.drone_controller.input_layer.drone_state import DroneState
from src.drone_controller.input_layer.drone_state_mapper import DroneStateMapper

UP_VECTOR = [0.0, 0.0, 1.0]

ZERO_VECTOR = [0.0, 0.0, 0.0]


class TestDroneStateMapper(TestCase):
    def test_keyboard_simple_up(self):
        position = UP_VECTOR
        rotation = ZERO_VECTOR
        velocity = UP_VECTOR
        velocity_ang = ZERO_VECTOR
        acceleration = UP_VECTOR
        acceleration_ang = ZERO_VECTOR

        expected_state = DroneState(position, rotation, velocity, velocity_ang, acceleration,
                                    acceleration_ang)

        position = ZERO_VECTOR
        velocity = ZERO_VECTOR
        acceleration = ZERO_VECTOR
        drone_state = DroneState(position, rotation, velocity, velocity_ang, acceleration,
                                 acceleration_ang)

        user_input = {"Rotation Forward": 0,
                      'Rotation Right': 0,
                      "Rotation Backward": 0,
                      "Rotation Left": 0,
                      "Acceleration": 1}

        mapper = DroneStateMapper()
        future_state: DroneState = mapper.keyboard(drone_state, user_input)

        self.assertEqual(future_state, expected_state, msg=f'Actual:\n'
                                                           f'{future_state.__str__()}\n\n'
                                                           f'Expected:\n'
                                                           f'{expected_state.__str__()}')
