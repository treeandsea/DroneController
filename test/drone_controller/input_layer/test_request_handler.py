from unittest import TestCase

from pytest import raises
import numpy as np
from drone_controller.exception.exceptions import UserInputError
from drone_controller.input_layer.drone_physics import DronePhysics
from drone_controller.input_layer.drone_state import DroneState
from drone_controller.input_layer.request_handler import RequestHandler

ZERO_VECTOR = np.array([0, 0, 0])
UP_VECTOR = np.array([0, 0, 1])

DRONE_STATE_ZERO = DroneState(ZERO_VECTOR, ZERO_VECTOR, ZERO_VECTOR, ZERO_VECTOR)


class RequestHandlerTest(TestCase):
    """
    Test the RequestHandler
    """

    def setUp(self) -> None:
        self.mass = 2
        self.max_rotor_thrust = 20
        radius = 1
        self.handler = RequestHandler("Quadrocopter", self.mass, self.max_rotor_thrust, radius)

    def test_simple_up_keyboard(self):
        """
        Tests a simple up input.
        """

        user_input = {'Rotation Forward': 0,
                      'Rotation Right': 0,
                      'Rotation Backward': 0,
                      'Rotation Left': 0,
                      'Acceleration': 1}

        expected_thrusts = [10.81 * self.mass / 4 / self.max_rotor_thrust] * 4

        thrusts: list = self.handler.keyboard_input(DRONE_STATE_ZERO, user_input)

        self.assertEqual(expected_thrusts, thrusts)

    def test_keyboard_input_exception(self):
        """
        Test if exception is thrown upon wrong user input.
        """
        with raises(UserInputError):
            user_input = {'velocity': [1, 1, 1]}
            self.handler.keyboard_input(DRONE_STATE_ZERO, user_input)

    def test_from_drone_physics(self):
        """
        Test if two request handler are equal.
        """
        # pylint: disable=protected-access
        drone_physics = DronePhysics(mass=2, thrust_per_rotor=20, radius=1, rotor_count=4)
        handler_from_physics: RequestHandler = RequestHandler.from_drone_physics('Quadrocopter',
                                                                                 drone_physics)
        thrust_calc = self.handler._thrust_calc
        other_calc = handler_from_physics._thrust_calc

        self.assertEqual(self.handler,
                         handler_from_physics,
                         msg=f'\n'
                             f'Expected:'
                             f'{thrust_calc.__dict__}'
                             f'\nActual:'
                             f'{other_calc.__dict__}')
        self.assertEqual(type(thrust_calc), type(other_calc))


class FeedBackRequestHandler(TestCase):
    """
    Tests the request handler with feedback.
    """

    def setUp(self) -> None:
        self.mass = 2
        self.max_rotor_thrust = 20
        radius = 1
        self.handler = RequestHandler("Quadrocopter", self.mass, self.max_rotor_thrust, radius,
                                      feedback=True)

    def test_feedback_simple_up(self):
        """
        Tests if the request handler ignores any diversions of the drone.
        """
        # pylint: disable=protected-access
        self.handler._previous_future_state = DroneState((0.1, 0.1, 0.), ZERO_VECTOR, ZERO_VECTOR,
                                                         ZERO_VECTOR, ZERO_VECTOR)
        user_input = {'Rotation Forward': 0,
                      'Rotation Right': 0,
                      'Rotation Backward': 0,
                      'Rotation Left': 0,
                      'Acceleration': 1}

        expected_thrusts = [10.81 * self.mass / 4 / self.max_rotor_thrust] * 4

        thrusts: list = self.handler.keyboard_input(DRONE_STATE_ZERO, user_input)

        self.assertEqual(len(expected_thrusts), len(thrusts))

        for expected, thrust in zip(expected_thrusts, thrusts):
            self.assertAlmostEqual(expected, thrust, delta=0.001)

    def test_reset(self):
        """
        Tests if the reset function is working.
        """
        # pylint: disable=protected-access
        user_input = {'Rotation Forward': 0,
                      'Rotation Right': 0,
                      'Rotation Backward': 0,
                      'Rotation Left': 0,
                      'Acceleration': 1}
        self.handler.keyboard_input(DRONE_STATE_ZERO, user_input)

        self.assertIsNotNone(self.handler._previous_future_state)
        self.handler.reset()
        self.assertIsNone(self.handler._previous_future_state)

    def test_stay_on_pos_airborne(self):
        """
        Tests if the request handler tries to stay at the same spot in the air.
        """
        # pylint: disable=protected-access

        user_input = {'Rotation Forward': 0,
                      'Rotation Right': 0,
                      'Rotation Backward': 0,
                      'Rotation Left': 0,
                      'Acceleration': 1}

        expected_thrusts = [(9.81 * self.mass) / 4] * 4

        self.handler.keyboard_input(DRONE_STATE_ZERO, user_input)

        user_input = {'Rotation Forward': 0,
                      'Rotation Right': 0,
                      'Rotation Backward': 0,
                      'Rotation Left': 0,
                      'Acceleration': 0}

        state = self.handler._previous_future_state
        self.handler.keyboard_input(state, user_input)

        state = self.handler._previous_future_state
        thrusts: list = self.handler.keyboard_input(state, user_input)

        self.assertEqual(len(expected_thrusts), len(thrusts))

        for expected, thrust in zip(expected_thrusts, thrusts):
            self.assertAlmostEqual(expected, thrust, delta=0.001)
