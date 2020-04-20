import math

import numpy as np

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

        if state['Position'] is not None:
            state['Position'] = add_lists(state['Position'], state['Velocity'])
        return DroneState.from_dict(state)

    @staticmethod
    def normalize_rotation(rotation) -> list:
        """
        Converts the drone rotation to values in [-1,1]
        :param rotation: 3D with angle values in degree
        :return: 3D vector
        """
        radians = np.radians(rotation)
        normalized_rotations = np.sin(radians)
        normalized_rotations[-1] = np.cos(radians[2])
        return normalized_rotations

    @staticmethod
    def acceleration(current_acceleration: iter, user_acceleration: float, rotation: iter) -> list:
        """
        Calculates the acceleration for the next state
        :param current_acceleration: the acceleration of the current state
        :param user_acceleration: the acceleration change for the next step
        :param rotation: the rotation for the next step
        :return: the acceleration of the next step
        """
        # only use the acceleration in drone direction
        current_acc = np.dot(current_acceleration, rotation)
        acc_vec = (current_acc + user_acceleration) * np.array(rotation)

        #acceleration = [angle * user_acceleration for angle in reversed(rotation[0:2])]
        #acceleration = add_lists(acceleration, current_acceleration[0:2])
        #length_z_acc = math.sqrt(math.pow(magnitude, 2) - math.pow(acceleration[0], 2) - math.pow(acceleration[1], 2))
        #acceleration.append(np.copysign(length_z_acc, magnitude))

        return acc_vec

    def angular_acceleration(self, state, user_input):
        """
        Calculates the angular acceleration of the next step.
        :param state: the current state of the drone
        :param user_input: the user input for the next step
        :return: the angular acceleration for the next step
        """
        angle_acc = state['Angular Acceleration']

        user_x = user_input['Rotation Right'] - user_input['Rotation Left']
        user_y = user_input['Rotation Forward'] - user_input['Rotation Backward']

        acc_x = angle_acc[0] + user_x * self._angle_per_step
        acc_y = angle_acc[0] + user_y * self._angle_per_step

        angle_acc_degree = np.array([acc_x, acc_y, angle_acc[2]])
        return np.sin(np.radians(angle_acc_degree))

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

        return np.array([rot_x, rot_y, rot_z])
