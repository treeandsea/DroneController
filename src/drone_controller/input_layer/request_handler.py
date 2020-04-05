"""
This module handles all requests. This will cover REST calls as well as native python calls.
"""
from src.drone_controller.calculation_layer.thrust_calculator import ThrustCalculatorQuadroCopter
from src.drone_controller.exception.exceptions import UserInputError
from src.drone_controller.input_layer.drone_state import DroneState
from src.drone_controller.input_layer.drone_state_mapper import DroneStateMapper


# pylint: disable=too-few-public-methods


class RequestHandler:
    """
    Handles request from python code.
    """

    def __init__(self, aircraft_type: str, mass: float, max_rotor_thrust: float, radius: float):
        """
        Initializes the request handler. This should always be the entry point.
        :param aircraft_type: Name of the vehicle type the thrust should be calculated for.
        :param mass: the mass of the vehicle
        :param max_rotor_thrust: The maximal thrust one rotor can produce. This will assume
        every rotor is the same.
        :param radius: the horizontal distance from the center of mass of each rotor. It will
        also assume it the same for every rotor.
        """
        if aircraft_type == 'Quadrocopter':
            self._thrust_calc = ThrustCalculatorQuadroCopter(mass, max_rotor_thrust, radius)
        else:
            raise NotImplementedError(f'This type {1} is not implemented yet',
                                      aircraft_type)

    def keyboard_input(self, drone_state: DroneState, user_input: dict) -> list:
        """
        Handles user input and will call the thrust calculator.
        :param drone_state: the momentary state of the drone
        :param user_input: keyboard input of the user
        :return: thrust list beginning from front and than clockwise
        """
        if not all(key in user_input for key in ["Rotation Forward",
                                                 "Rotation Right",
                                                 "Rotation Backward",
                                                 "Rotation Left",
                                                 "Acceleration"]):
            raise UserInputError(user_input, "The keyboard input is complete.")

        state_mapper = DroneStateMapper()
        expected_state = state_mapper.keyboard(drone_state, user_input)
        return self._calc(drone_state, expected_state)

    def _calc(self, drone_state, expected_state):
        """
        Calls to the thrust calculator to compute the thrust for four rotors.
        :return: thrusts for four rotor
        """
        return self._thrust_calc.calc(drone_state, expected_state)
