"""
This module handles all requests. This will cover REST calls as well as native python calls.
"""
from src.drone_controller.calculation_layer.thrust_calculator import ThrustCalculatorQuadroCopter
from src.drone_controller.exception.exceptions import UserInputError
from src.drone_controller.input_layer.drone_state import DroneState
from src.drone_controller.input_layer.drone_state_mapper import DroneStateMapper


class RequestHandler:
    """
    Handles request from python code.
    """

    def __init__(self, aircraft_type):
        if aircraft_type == 'Quadrocopter':
            self._thrust_calc = ThrustCalculatorQuadroCopter()
        else:
            raise NotImplementedError(f'This type {1} is not implemented yet',
                                      aircraft_type)

    def keyboard_input(self, drone_state: DroneState, user_input: dict):
        """
        Handles user input and will call the thrust calculator.
        :param drone_state: the momentary state of the drone
        :param user_input: keyboard input of the user
        """
        if not all(key in user_input for key in ["Rotation Forward",
                                                 "Rotation Right",
                                                 "Rotation Backward",
                                                 "Rotation Left",
                                                 "Acceleration"]):
            raise UserInputError(user_input, "The keyboard input is complete.")

        state_mapper = DroneStateMapper()
        expected_state = state_mapper.keyboard(user_input)
        return self._calc(drone_state, expected_state)

    def _calc(self, drone_state, expected_state):
        """
        Calls to the thrust calculator to compute the thrust for four rotors.
        :return: thrusts for four rotor
        """
        return self._thrust_calc.calc(drone_state, expected_state)
