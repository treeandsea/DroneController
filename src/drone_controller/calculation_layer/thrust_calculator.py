# pylint: disable=too-few-public-methods
import abc

import numpy

from src.drone_controller.input_layer.drone_state import DroneState

GRAVITATIONAL_ACCELERATION = 9.81


class ThrustCalculator(metaclass=abc.ABCMeta):
    """
    Interface for thrust calculators.
    """

    @abc.abstractmethod
    def calc(self, current_state: DroneState, future_state: DroneState) -> list:
        """
        Calculates the thrust for an object.
        :param current_state: the state of drone now
        :param future_state: the desired state of the drone
        :return: relative thrusts values (for DC rotors)
        """
        raise NotImplementedError


class ThrustCalculatorQuadroCopter(ThrustCalculator):
    """
    Calculates thrusts for a quadro copter.
    """

    def __init__(self, mass: float, rotor_thrust: float, radius: float):
        self.mass = mass
        self.rotor_thrust = rotor_thrust
        self.radius = radius

    def calc(self, current_state: DroneState, future_state: DroneState) -> list:
        """
        The actual calculation.
        :param current_state: the state of drone now
        :param future_state: the desired state of the drone
        :return: four relative thrusts values (for DC rotors)
        """
        jerk = self.subtract_lists(future_state.state_dict['Acceleration'],
                                   current_state.state_dict['Acceleration'])

        jerk_ang = self.subtract_lists(future_state.state_dict['Angular Acceleration'],
                                       current_state.state_dict['Angular Acceleration'])

        needed_acceleration = jerk[0:2]
        needed_acceleration.append(jerk[2] + GRAVITATIONAL_ACCELERATION)
        force = [x * self.mass for x in needed_acceleration]

        thrust_per_rotor = [(numpy.linalg.norm(force) / 4) / self.rotor_thrust] * 4

        # Add torque
        thrust_per_rotor[0] = thrust_per_rotor[0] + jerk_ang[1] * self.mass * self.radius / 2
        thrust_per_rotor[1] = thrust_per_rotor[1] + jerk_ang[0] * self.mass * self.radius / 2
        thrust_per_rotor[2] = thrust_per_rotor[2] - jerk_ang[1] * self.mass * self.radius / 2
        thrust_per_rotor[3] = thrust_per_rotor[3] - jerk_ang[0] * self.mass * self.radius / 2

        return thrust_per_rotor

    @staticmethod
    def subtract_lists(first_list, second_list):
        """
        Subtracts two lists
        :param first_list:
        :param second_list:
        :return: one list
        """
        return [x - y for x, y in zip(first_list, second_list)]

    @staticmethod
    def add_lists(first, second):
        """
        Adds two lists
        :param first:
        :param second:
        :return: one list
        """
        return [sum(x) for x in zip(first, second)]
