from unittest import TestCase

from src.drone_controller.input_layer.drone_state import DroneState
from src.drone_controller.input_layer.drone_state_mapper import DroneStateMapper


class TestDroneStateMapper(TestCase):
    def test_keyboard_simple_up(self):
        position = [0, 0, 1]
        rotation = [0, 0, 0]
        velocity = [0, 0, 1]
        velocity_ang = [0, 0, 0]
        acceleration = [0, 0, 1]
        acceleration_ang = [0, 0, 0]

        expected_state = DroneState(position, rotation, velocity, velocity_ang, acceleration,
                                    acceleration_ang)

        position = [0, 0, 0]
        velocity = [0, 0, 0]
        acceleration = [0, 0, 0]
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
