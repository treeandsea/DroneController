# pylint: disable=too-few-public-methods
from src.drone_controller.input_layer.drone_state import DroneState


class ThrustCalculatorQuadroCopter:
    """
    Calculator for rotor thrusts.
    """

    def calc(self, drone_state: DroneState, expected_state: DroneState):
        """
        Calculates the thrust.
        :param drone_state: the momentary drone state
        :param expected_state: the expected state of the drone
        """
        raise NotImplementedError
