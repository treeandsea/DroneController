from unittest import TestCase

from src.drone_controller.calculation_layer.ThrustCalculator import ThrustCalculatorQuadroCopter
from src.drone_controller.input_layer.drone_state import DroneState

ZERO_VECTOR = [0, 0, 0]
UP_VECTOR = [0, 0, 1]


class QuadroCopterTest(TestCase):
    def setUp(self):
        """
        Sets up the calculator with a drone weight and the max thrust per rotor.
        """
        weight = 2.0  # kg
        rotor_thrust = 20.0  # Newton
        self.calculator = ThrustCalculatorQuadroCopter(weight, rotor_thrust)

    def test_calc_simple_up(self):
        """
        Tests the thrust calculation for drone from ground one meter up.
        """
        position = ZERO_VECTOR
        rotation = ZERO_VECTOR
        velocity = ZERO_VECTOR
        velocity_ang = ZERO_VECTOR
        acceleration = ZERO_VECTOR
        acceleration_ang = ZERO_VECTOR
        current_state = DroneState(position, rotation, velocity, velocity_ang, acceleration,
                                   acceleration_ang)

        position = UP_VECTOR
        velocity = UP_VECTOR
        acceleration = UP_VECTOR
        future_state = DroneState(position, rotation, velocity, velocity_ang, acceleration,
                                  acceleration_ang)

        needed_thrust = 21.61  # Newton
        relative_thrust_per_rotor = (needed_thrust / 4) / self.calculator.rotor_thrust
        expected_thrusts = [relative_thrust_per_rotor] * 4

        thrusts = self.calculator.calc(current_state, future_state)

        self.assertEqual(expected_thrusts, thrusts)
