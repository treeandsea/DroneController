import abc

import numpy

from src.drone_controller.input_layer.drone_state import DroneState

GRAVITATIONAL_ACCELERATION = 9.81


class ThrustCalculator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calc(self, current_state: DroneState, future_state: DroneState) -> list:
        raise NotImplementedError


class ThrustCalculatorQuadroCopter(ThrustCalculator):
    def __init__(self, weight: float, rotor_thrust: float):
        self.weight = weight
        self.rotor_thrust = rotor_thrust

    def calc(self, current_state: DroneState, future_state: DroneState) -> list:
        jerk = self.subtract_lists(future_state.state_dict['Acceleration'],
                                   current_state.state_dict[
                                       'Acceleration'])

        needed_acceleration = jerk[0:2]
        needed_acceleration.append(jerk[2] + GRAVITATIONAL_ACCELERATION)
        force = [x * self.weight for x in needed_acceleration]

        return [(numpy.linalg.norm(force) / 4) / self.rotor_thrust] * 4

    @staticmethod
    def subtract_lists(first_list, second_list):
        return [x - y for x, y in zip(first_list, second_list)]

    @staticmethod
    def add_lists(first, second):
        return [sum(x) for x in zip(first, second)]
