import abc

from src.drone_controller.input_layer.drone_state import DroneState


class ThrustCalculator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calc(self, current_state: DroneState, future_state: DroneState) -> list:
        raise NotImplementedError


class ThrustCalculatorQuadroCopter(ThrustCalculator):
    def __init__(self, weight: float, rotor_thrust: float):
        self.weight = weight
        self.rotor_thrust = rotor_thrust

    def calc(self, current_state: DroneState, future_state: DroneState) -> list:
        pass
