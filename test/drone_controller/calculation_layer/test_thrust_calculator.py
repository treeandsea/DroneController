from unittest import TestCase

from drone_controller.calculation_layer.thrust_calculator import ThrustCalculatorQuadroCopter
from drone_controller.input_layer.drone_state import DroneState

ZERO_VECTOR = [0, 0, 0]
UP_VECTOR = [0, 0, 1]


class QuadroCopterTest(TestCase):
    """
    Tests the thrust calculator for quadro copters.
    """

    def setUp(self):
        """
        Sets up the calculator with a drone mass and the max thrust per rotor.
        """
        mass = 2.0  # kg
        rotor_thrust = 20.0  # Newton
        radius = 1  # m
        self.calculator = ThrustCalculatorQuadroCopter(mass, rotor_thrust, radius)

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
        current_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                   velocity_ang)

        position = UP_VECTOR
        velocity = UP_VECTOR
        acceleration = UP_VECTOR
        future_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                  velocity_ang)

        needed_thrust = 21.61  # Newton
        relative_thrust_per_rotor = (needed_thrust / 4) / self.calculator.max_rotor_thrust
        expected_thrusts = [relative_thrust_per_rotor] * 4

        thrusts = self.calculator.calc(current_state, future_state)

        for expected_thrust, thrust in zip(expected_thrusts, thrusts):
            self.assertAlmostEqual(expected_thrust, thrust, delta=0.001)

    def test_up_with_rotation(self):
        """
        Tests if the correct rotors uses more power than the opposite site.
        """
        position = ZERO_VECTOR
        rotation = ZERO_VECTOR
        velocity = ZERO_VECTOR
        velocity_ang = ZERO_VECTOR
        acceleration = ZERO_VECTOR
        acceleration_ang = ZERO_VECTOR
        current_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                   velocity_ang)

        position = [0, 0.174, 0.985]
        rotation = [10, 0, 0]
        velocity = [0, 0.174, 0.985]
        velocity_ang = [0.174, 0, 0]
        acceleration = [0, 0.174, 0.985]
        acceleration_ang = [0.174, 0, 0]
        future_state = DroneState(rotation, velocity, acceleration, acceleration_ang, position,
                                  velocity_ang)

        thrusts = self.calculator.calc(current_state, future_state)

        print(thrusts)
        self.assertGreater(thrusts[1], thrusts[3])
        self.assertAlmostEqual(thrusts[0], thrusts[2])
