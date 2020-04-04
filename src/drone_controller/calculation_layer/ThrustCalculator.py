import abc

from src.drone_controller.input_layer.drone_state import DroneState


class ThrustCalculator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def calc(self, current_state: DroneState, future_state: DroneState) -> list:
        raise NotImplementedError


class ThrustCalculatorQuadroCopter(ThrustCalculator):
    def calc(self, current_state: DroneState, future_state: DroneState) -> list:
        pass
