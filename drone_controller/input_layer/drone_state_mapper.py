import math

import numpy

from drone_controller.input_layer.drone_state import DroneState
from drone_controller.util.list_operators import add_lists


class DroneStateMapper:
    """
    Maps different inputs to a drone state.
    """

    def __init__(self, angle_per_step=10):
        self._angle_per_step = angle_per_step

    def keyboard(self, current_state: DroneState, user_input: dict):
        """
        Maps keyboard input to a drone state. The mapper uses fictional units and the time until
        next expected state is one time unit. So the steps below are basically integrations.
        :param current_state: the current state of the drone
        :param user_input: keyboard input from user
        :return: the expected state of the drone
        """
        state: dict = current_state.state_dict
        state['Rotation'] = self.add_rotation(state['Rotation'], user_input)
        rotation_normalized = self.normalize_rotation(state['Rotation'])

        state['Angular Acceleration'] = self.angular_acceleration(state, user_input)

        state['Acceleration'] = self.acceleration(state['Acceleration'], user_input[
            'Acceleration'], rotation_normalized)

        state['Velocity'] = add_lists(state['Velocity'], state['Acceleration'])
        state['Angular Velocity'] = add_lists(state['Angular Velocity'],
                                              state['Angular Acceleration'])

        state['Position'] = add_lists(state['Position'], state['Velocity'])
        return DroneState.from_dict(state)

    @staticmethod
    def normalize_rotation(rotation) -> list:
        """
        Converts the drone rotation to values in [-1,1]
        :param rotation: 3D with angle values in degree
        :return: 3D vector
        """
        radians = list([math.radians(x) for x in rotation])
        normalized_rotations = list([math.sin(x) for x in radians[0:2]])
        normalized_rotations.append(math.cos(rotation[2]))
        return normalized_rotations

    @staticmethod
    def acceleration(current_acceleration, user_acceleration, rotation):
        """
        Calculates the acceleration for the next state
        :param current_acceleration: the acceleration of the current state
        :param user_acceleration: the accelerationn change for the next step
        :param rotation: the rotation for the next step
        :return: the acceleration of the next step
        """
        current = numpy.array(current_acceleration)
        magnitude = numpy.linalg.norm(current) + user_acceleration
        acceleration = [angle * user_acceleration for angle in reversed(rotation[0:2])]
        acceleration = add_lists(acceleration, current_acceleration[0:2])
        acceleration.append(math.sqrt(math.pow(magnitude, 2) - math.pow(acceleration[0], 2) -
                                      math.pow(acceleration[1], 2)))
        return acceleration

    def angular_acceleration(self, state, user_input):
        """
        Calculates the angular acceleration of the next step.
        :param state: the current state of the drone
        :param user_input: the user input for the next step
        :return: the angular acceleration for the next step
        """
        acceleration = state['Angular Acceleration']

        user_x = user_input['Rotation Right'] - user_input['Rotation Left']
        user_y = user_input['Rotation Forward'] - user_input['Rotation Backward']

        acc_x = acceleration[0] + user_x * self._angle_per_step
        acc_y = acceleration[0] + user_y * self._angle_per_step

        acceleration_degree = [acc_x, acc_y, acceleration[2]]
        return [math.sin(math.radians(x)) for x in acceleration_degree]

    def add_rotation(self, rotation, user_input):
        """
        Adds rotation from state and user input together.
        :param rotation: in degree
        :param user_input:
        :return:
        """
        user_x = user_input['Rotation Right'] - user_input['Rotation Left']
        user_y = user_input['Rotation Forward'] - user_input['Rotation Backward']

        rot_x = rotation[0] + user_x * self._angle_per_step
        rot_y = rotation[1] + user_y * self._angle_per_step
        rot_z = rotation[2]

        return [rot_x, rot_y, rot_z]
