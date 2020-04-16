"""
This module handles all requests. This will cover REST calls as well as native python calls.
"""

# pylint: disable=too-many-arguments
from drone_controller.calculation_layer.thrust_calculator import ThrustCalculatorQuadroCopter
from drone_controller.exception.exceptions import UserInputError
from drone_controller.input_layer.drone_physics import DronePhysics
from drone_controller.input_layer.drone_state import DroneState
from drone_controller.input_layer.drone_state_mapper import DroneStateMapper


class RequestHandler:
    """
    Handles request from python code.
    """

    def __init__(self, aircraft_type: str, mass: float, max_rotor_thrust: float, radius: float,
                 feedback: bool = False):
        """
        Initializes the request handler. This should always be the entry point.
        :param aircraft_type: Name of the vehicle type the thrust should be calculated for.
        :param mass: the mass of the vehicle
        :param max_rotor_thrust: The maximal thrust one rotor can produce. This will assume
        every rotor is the same.
        :param radius: the horizontal distance from the center of mass of each rotor. It will
        also assume it the same for every rotor.
        :param feedback: activates a feed back loop
        """
        if aircraft_type == 'Quadrocopter':
            self._thrust_calc = ThrustCalculatorQuadroCopter(mass, max_rotor_thrust, radius)
        else:
            raise NotImplementedError(f'This type {1} is not implemented yet',
                                      aircraft_type)

        self.feedback = feedback
        self._previous_future_state = None

    @classmethod
    def from_drone_physics(cls, aircraft_type: str,
                           drone_physics: DronePhysics,
                           feedback: bool = False):
        """
        Creates a request handler from drone physics.
        :param feedback: flag for using state calculation with feedback loops.
        :param aircraft_type: Name of the vehicle type the thrust should be calculated for.
        :param drone_physics: wrapper of the physics of the drone
        :return: a request handler
        """
        physics_dict = drone_physics.physics_dict()
        return cls(aircraft_type,
                   physics_dict['mass'],
                   physics_dict['thrust_per_rotor'],
                   physics_dict['radius'],
                   feedback)

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
        if self.feedback:
            previous_future_state = self._previous_future_state or drone_state

            expected_state = state_mapper.keyboard(previous_future_state, user_input)
            self._previous_future_state = expected_state
        else:
            expected_state = state_mapper.keyboard(drone_state, user_input)
        return self._calc(drone_state, expected_state)

    def _calc(self, drone_state, expected_state):
        """
        Calls to the thrust calculator to compute the thrust for four rotors.
        :return: thrusts for four rotor
        """
        return self._thrust_calc.calc(drone_state, expected_state)

    def __eq__(self, other):
        if not isinstance(other, RequestHandler):
            return False

        return other._thrust_calc.__dict__ == self._thrust_calc.__dict__
