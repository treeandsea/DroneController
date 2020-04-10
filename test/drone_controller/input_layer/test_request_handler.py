from unittest import TestCase

from pytest import raises

from drone_controller.exception.exceptions import UserInputError
from drone_controller.input_layer.drone_physics import DronePhysics
from drone_controller.input_layer.drone_state import DroneState
from drone_controller.input_layer.request_handler import RequestHandler


class RequestHandlerTest(TestCase):
    """
    Test the RequestHandler
    """

    def setUp(self) -> None:
        mass = 2
        max_rotor_thrust = 20
        radius = 1
        self.handler = RequestHandler("Quadrocopter", mass, max_rotor_thrust, radius)

        drone_state = DroneState([0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0])

        user_input = {'Rotation Forward': 0,
                      'Rotation Right': 0,
                      'Rotation Backward': 0,
                      'Rotation Left': 0,
                      'Acceleration': 1}

        expected_thrusts = [10.81 * mass / 4 / max_rotor_thrust] * 4

        thrusts: list = self.handler.keyboard_input(drone_state, user_input)

        self.assertEqual(expected_thrusts, thrusts)

    def test_keyboard_input_exception(self):
        """
        Test if exception is thrown upon wrong user input.
        """
        with raises(UserInputError):
            drone_state = DroneState([0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                                     [0, 0, 0])
            user_input = {'velocity': [1, 1, 1]}
            self.handler.keyboard_input(drone_state, user_input)

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
