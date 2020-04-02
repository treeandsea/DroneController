import math

from src.drone_controller.input_layer.drone_state import DroneState


class DroneStateMapper:
    """
    Maps different inputs to a drone state.
    """

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

        acceleration = [i * user_input['Acceleration'] for i in rotation_normalized]
        state['Acceleration'] = self.add_lists(state['Acceleration'], acceleration)

        state['Velocity'] = self.add_lists(state['Velocity'], state['Acceleration'])

        state['Position'] = self.add_lists(state['Position'], state['Velocity'])
        return DroneState.from_dict(state)

    @staticmethod
    def multiply_lists(first_list, second_list):
        """
        Multiplies two lists element wise
        :param first_list:
        :param second_list:
        :return:
        """
        return [a * b for a, b in zip(first_list, second_list)]

    @staticmethod
    def normalize_rotation(rotation) -> list:
        """
        Converts the drone rotation to values in [-1,1]
        :param rotation: 3D with angle values
        :return: 3D vector
        """
        normalized_rotations = list([math.sin(x) for x in rotation[0:2]])
        normalized_rotations.append(math.cos(rotation[2]))
        return normalized_rotations

    @staticmethod
    def add_lists(first_list, second_list):
        """
        Adds two lists element wise
        :param first_list:
        :param second_list:
        :return:
        """
        return [sum(x) for x in zip(first_list, second_list)]

    @staticmethod
    def add_rotation(rotation, user_input):
        """
        Adds rotation from state and user input together.
        :param rotation:
        :param user_input:
        :return:
        """
        rot_x = rotation[0] + user_input['Rotation Right'] - user_input['Rotation Left']
        rot_y = rotation[1] + user_input['Rotation Forward'] - user_input['Rotation Backward']
        rot_z = rotation[2]

        return [rot_x, rot_y, rot_z]
