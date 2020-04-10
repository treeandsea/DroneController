from unittest import TestCase

from drone_controller.input_layer.drone_state import DroneState
from drone_controller.input_layer.drone_state_mapper import DroneStateMapper

ONE_UP = {"Rotation Forward": 0,
          'Rotation Right': 0,
          "Rotation Backward": 0,
          "Rotation Left": 0,
          "Acceleration": 1}

UP_VECTOR = [0.0, 0.0, 1.0]

ZERO_VECTOR = [0.0, 0.0, 0.0]


class TestDroneStateMapper(TestCase):
    """
    Tests the drone state mapper.
    """

    def setUp(self):
        """
        Sets up the drone state mapper.
        """
        self.mapper = DroneStateMapper()

    def test_keyboard_simple_up(self):
        """
        Tests one time step from drone on ground with everything zero.
        """
        position = UP_VECTOR
        rotation = ZERO_VECTOR
        velocity = UP_VECTOR
        velocity_ang = ZERO_VECTOR
        acceleration = UP_VECTOR
        acceleration_ang = ZERO_VECTOR

        expected_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                    velocity_ang)

        position = ZERO_VECTOR
        velocity = ZERO_VECTOR
        acceleration = ZERO_VECTOR
        drone_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                 velocity_ang)

        user_input = ONE_UP

        future_state: DroneState = self.mapper.keyboard(drone_state, user_input)

        self.assertEqual(future_state, expected_state, msg=f'Actual:\n'
                                                           f'{future_state.__str__()}\n\n'
                                                           f'Expected:\n'
                                                           f'{expected_state.__str__()}')

    def test_keyboard_up_from_position(self):
        """
        Tests the drone in the air but everything else zero.
        """
        position = [2, 3, 4]
        rotation = ZERO_VECTOR
        velocity = ZERO_VECTOR
        velocity_ang = ZERO_VECTOR
        acceleration = ZERO_VECTOR
        acceleration_ang = ZERO_VECTOR

        drone_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                 velocity_ang)

        user_input = ONE_UP

        position = [2, 3, 5]
        velocity = UP_VECTOR
        acceleration = UP_VECTOR

        expected_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                    velocity_ang)

        future_state: DroneState = self.mapper.keyboard(drone_state, user_input)

        self.assertEqual(future_state, expected_state, msg=f'Actual:\n'
                                                           f'{future_state.__str__()}\n\n'
                                                           f'Expected:\n'
                                                           f'{expected_state.__str__()}')

    def test_rotation_from_ground(self):
        """
        Tests from the standing drone to drone in air with rotation.
        """
        position = ZERO_VECTOR
        rotation = ZERO_VECTOR
        velocity = ZERO_VECTOR
        velocity_ang = ZERO_VECTOR
        acceleration = ZERO_VECTOR
        acceleration_ang = ZERO_VECTOR

        drone_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                 velocity_ang)

        position = [0, 0.174, 0.985]
        rotation = [10.0, 0.0, 0.0]
        velocity = [0, 0.174, 0.985]
        velocity_ang = [0.174, 0.0, 0.0]  # rad/s
        acceleration = [0, 0.174, 0.985]
        acceleration_ang = [0.174, 0.0, 0.0]  # rad/s^2

        expected_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                    velocity_ang)

        user_input = {"Rotation Forward": 0,
                      'Rotation Right': 1,
                      "Rotation Backward": 0,
                      "Rotation Left": 0,
                      "Acceleration": 1}

        future_state: DroneState = self.mapper.keyboard(drone_state, user_input)

        self.assertEqual(future_state, expected_state, msg=f'Actual:\n'
                                                           f'{future_state.__str__()}\n\n'
                                                           f'Expected:\n'
                                                           f'{expected_state.__str__()}')
