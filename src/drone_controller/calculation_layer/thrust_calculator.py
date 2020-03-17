# pylint: disable=too-few-public-methods
class ThrustCalculator:
    """
    Calculator for rotor thrusts.
    """

    def __init__(self, drone_state, expected_state):
        """
        :param drone_state: the momentary drone state
        :param expected_state: the expected state of the dron
        """
        self.drone_state = drone_state
        self.expected_state = expected_state

    def calc(self, rotor_count):
        """
        Calculates the thrust.
        :param rotor_count: the number of rotors the calculator should calculate.
        """
        raise NotImplementedError
