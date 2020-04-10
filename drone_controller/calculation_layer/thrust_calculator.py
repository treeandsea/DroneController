# pylint: disable=too-few-public-methods
import abc

import numpy

from drone_controller.input_layer.drone_state import DroneState
from drone_controller.util.list_operators import subtract_lists

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

    def __init__(self, mass: float, max_rotor_thrust: float, radius: float,
                 inertia_flattening: float = 1):
        self.mass = mass
        self.max_rotor_thrust = max_rotor_thrust
        self.radius = radius
        self.inertia_flattening = inertia_flattening

    def calc(self, current_state: DroneState, future_state: DroneState) -> list:
        """
        The actual calculation. This uses fictional units and assume the the future step is one time
        step away. So therefore the calculation below are integrations and acceleration
        subtraction is jerk.
        :param current_state: the state of drone now
        :param future_state: the desired state of the drone
        :return: four relative thrusts values (for DC rotors)
        """
        jerk = subtract_lists(future_state.state_dict['Acceleration'],
                              current_state.state_dict['Acceleration'])

        jerk_ang = subtract_lists(future_state.state_dict['Angular Acceleration'],
                                  current_state.state_dict['Angular Acceleration'])

        needed_acceleration = jerk[0:2]
        needed_acceleration.append(jerk[2] + GRAVITATIONAL_ACCELERATION)
        force = [x * self.mass for x in needed_acceleration]

        thrust_per_rotor = [(numpy.linalg.norm(force) / 4) / self.max_rotor_thrust] * 4

        # Add torque
        inertia_torque = self.mass * self.radius / (2 * self.inertia_flattening)

        thrust_per_rotor[0] = thrust_per_rotor[0] + jerk_ang[1] * inertia_torque
        thrust_per_rotor[1] = thrust_per_rotor[1] + jerk_ang[0] * inertia_torque
        thrust_per_rotor[2] = thrust_per_rotor[2] - jerk_ang[1] * inertia_torque
        thrust_per_rotor[3] = thrust_per_rotor[3] - jerk_ang[0] * inertia_torque

        return thrust_per_rotor
