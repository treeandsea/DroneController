import math


class DronePhysics:
    """
    Wrapper class for the physics of a drone.
    """
    __slots__ = ['mass', 'thrust_per_rotor', 'rotor_count', 'radius']

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def physics_dict(self):
        """
        :return: the drone physics in a dict
        """
        # pylint: disable=no-member
        return dict(mass=self.mass, thrust_per_rotor=self.thrust_per_rotor,
                    rotor_count=self.rotor_count, radius=self.radius)

    def __eq__(self, other, float_precision=0.001):
        """
        Checks if two drone physics are equal.
        :param other: the other object to check
        :param float_precision: how precise floats should be checked
        :return: bool
        """
        if not isinstance(other, DronePhysics):
            raise TypeError(f'other is not DronePhysics but {type(other)}.')
        physics_dict = self.physics_dict()
        other_dict = other.physics_dict()
        if len(physics_dict) != len(other_dict):
            return False

        for (keys, physics_values, other_values) in zip(physics_dict.keys(),
                                                        physics_dict.values(),
                                                        other_dict.values()):

            if math.fabs(physics_values - other_values) > float_precision:
                print(f'Unequal at {keys} {physics_values} != {other_values}')
                return False
        return True
