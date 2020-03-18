from unittest import TestCase, skip
from unittest.mock import Mock

from pytest import raises

from src.drone_controller.exception.exceptions import UserInputError
from src.drone_controller.input_layer.drone_state import DroneState
from src.drone_controller.input_layer.request_handler import RequestHandler


class RequestHandlerTest(TestCase):
    """
    Test the RequestHandler
    """

    def setUp(self) -> None:
        self.handler = RequestHandler("Quadrocopter")

    @skip("Not enough dependencies implemented.")
    def test_keyboard_input(self):
        """
        Test if a thrust dictionary for a quadrocopter is returned.
        """
        raise NotImplementedError("Too much stuff is missing right now.")

    def test_keyboard_input_exception(self):
        """
        Test if exception is thrown upon wrong user input.
        """
        with raises(UserInputError):
            drone_state = Mock(DroneState)
            user_input = {'velocity': [1, 1, 1]}
            self.handler.keyboard_input(drone_state, user_input)
