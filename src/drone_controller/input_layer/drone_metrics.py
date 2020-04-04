import math


class DroneMetrics:
    __slots__ = ['mass', 'thrust_per_rotor', 'rotor_count', 'radius']

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __dict__(self):
        """
        :return: the drone metrics in a dict
        """
        return {'mass': self.mass,
                'thrust_per_rotor': self.thrust_per_rotor,
                'rotor_count': self.rotor_count,
                'radius': self.radius}

    def __eq__(self, other, float_precision=0.001):
        if not isinstance(other, DroneMetrics):
            raise TypeError(f'other is not DroneMetrics but {type(other)}.')
        if len(self.__dict__()) != len(other.__dict__()):
            return False

        for (keys, metric_values, other_values) in zip(self.__dict__().keys(),
                                                       self.__dict__().values(),
                                                       other.__dict__().values()):

            if math.fabs(metric_values - other_values) > float_precision:
                print(f'Unequal at {keys} {metric_values} != {other_values}')
                return False
        return True
