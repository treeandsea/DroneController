# pylint: disable=too-many-arguments
# a wrapper class needs more parameter
import math

from drone_controller.exception.exceptions import DroneControllerError


def check_input(parameter, name):
    """
    Checks a parameter if it's three dimensional.
    :param parameter: the parameter itself
    :param name: it's name for error printing
    """
    if not len(parameter) == 3:
        raise DroneStateError('DroneState.create()',
                              (f'The input {1} is invalid {2}',
                               name,
                               parameter))


# pylint: disable=too-few-public-methods
class DroneState:
    """
    Wrapper class for the state of the drone.
    """

    def __init__(self, rotation, velocity, acceleration, acceleration_ang, position=(0., 0., 0.),
                 velocity_ang=(0., 0., 0.)):
        """
        Uses a three dimensional position vector, containing x,y,z coordinates.
        :param position: 3D vector of the drone's position
        :param rotation: 3D vector of the drone's rotation
        :param velocity: 3D vector of the drone's translation velocity
        :param velocity_ang: 3D vector of the drone's angular velocity
        :param acceleration: 3D vector of the drone's translation acceleration
        :param acceleration_ang: 3D vector of the drone's angular acceleration
        """
        check_input(position, 'position')
        check_input(rotation, 'rotation')
        check_input(velocity, 'velocity')
        check_input(velocity_ang, 'angular velocity')
        check_input(acceleration, 'acceleration')
        check_input(acceleration_ang, 'angular acceleration')
        self._position = position
        self._rotation = rotation
        self._velocity = velocity
        self._velocity_ang = velocity_ang
        self._acceleration = acceleration
        self._acceleration_ang = acceleration_ang
        self._float_precision = 0.001

    @property
    def float_precision(self):
        """
        :return: The precision of floats while comparing two drone states.
        """
        return self._float_precision

    @float_precision.setter
    def float_precision(self, value):
        if not isinstance(value, float):
            raise TypeError(f'float_precision must be a float, but was {type(value)}.')
        self._float_precision = value

    @property
    def state_dict(self):
        """
        Maps the drone state to a dictionary.
        :param self: this drone state
        :return: dictionary
        """
        return {
            "Position": self._position,
            "Rotation": self._rotation,
            "Velocity": self._velocity,
            "Angular Velocity": self._velocity_ang,
            "Acceleration": self._acceleration,
            "Angular Acceleration": self._acceleration_ang
        }

    @classmethod
    def from_dict(cls, state: dict):
        """
        Creates a drone state from dict.
        :param state: dict with drone state fields
        :return: a DroneState instance
        """
        position = state['Position']
        rotation = state['Rotation']
        velocity = state['Velocity']
        velocity_ang = state['Angular Velocity']
        acceleration = state['Acceleration']
        acceleration_ang = state['Angular Acceleration']
        return cls(rotation, velocity, acceleration,
                   acceleration_ang, position, velocity_ang)

    def __str__(self):
        """
        Prints the key-value-pairs.
        :return: use the dict as return value
        """
        return self.state_dict

    def __eq__(self, other):
        """
        Checks if the values in the other DroneState are equal.
        :param other: the other DroneState to compare to
        :return: boolean for equality
        """
        if not isinstance(other, DroneState):
            return False
        state_dict = self.state_dict
        other_state_dict = other.state_dict

        if state_dict.__len__() != other_state_dict.__len__():
            return False

        for (keys, state_values, other_values) in zip(state_dict.keys(), state_dict.values(),
                                                      other_state_dict.values()):
            for a_item, b_item in zip(state_values, other_values):
                if math.fabs(a_item - b_item) > self._float_precision:
                    print(f'Unequal at {keys} {a_item} != {b_item}')
                    return False
        return True


class DroneStateError(DroneControllerError):
    """
    Invalid drone state.
    """

    def __init__(self, expression, message):
        """
        Is raised when the drone state receives invalid data.
        :rtype: DroneStateError
        """
        super().__init__()
        self.expression = expression
        self.message = message
