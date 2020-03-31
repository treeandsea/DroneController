# pylint: disable=too-many-arguments
# a wrapper class needs more parameter
from src.drone_controller.exception.exceptions import DroneControllerError


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

    def __init__(self, position, rotation, velocity, velocity_ang, acceleration, acceleration_ang):
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
        return cls(position, rotation, velocity, velocity_ang, acceleration,
                   acceleration_ang)

    def __str__(self):
        """
        Prints the key-value-pairs.
        :return: use the dict as return value
        """
        return self.state_dict


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
