import math


class DroneMetrics:
    """
    Wrapper class for the metrics of a drone.
    """
    __slots__ = ['mass', 'thrust_per_rotor', 'rotor_count', 'radius']

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def metrics_dict(self):
        """
        :return: the drone metrics in a dict
        """
        # pylint: disable=no-member
        return dict(mass=self.mass, thrust_per_rotor=self.thrust_per_rotor,
                    rotor_count=self.rotor_count, radius=self.radius)

    def __eq__(self, other, float_precision=0.001):
        """
        Checks if two drone metrics are equal.
        :param other: the other object to check
        :param float_precision: how precise floats should be checked
        :return: bool
        """
        if not isinstance(other, DroneMetrics):
            raise TypeError(f'other is not DroneMetrics but {type(other)}.')
        metrics_dict = self.metrics_dict()
        other_dict = other.metrics_dict()
        if len(metrics_dict) != len(other_dict):
            return False

        for (keys, metric_values, other_values) in zip(metrics_dict.keys(),
                                                       metrics_dict.values(),
                                                       other_dict.values()):

            if math.fabs(metric_values - other_values) > float_precision:
                print(f'Unequal at {keys} {metric_values} != {other_values}')
                return False
        return True
