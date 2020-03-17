class DroneState:
    def __init__(self, position, velocity, velocity_ang, acceleration, acceleration_ang):
        self._position = position
        self._velocity = velocity
        self._velocity_ang = velocity_ang
        self._acceleration = acceleration
        self._acceleration_ang = acceleration_ang

        @property
        def state(self):
            """
            Maps the drone state to a dictionary.
            :param self: this drone state
            :return: dictionary
            """
            return {
                "Position": self._position,
                "Velocity": self._velocity,
                "Angular Velocity": self._velocity_ang,
                "Acceleration": self._acceleration,
                "Angular Acceleration": self._acceleration_ang
            }

    @classmethod
    def create(cls, position, velocity, velocity_ang, acceleration, acceleration_ang):
        """
        Uses a three dimensional position vector, containing x,y,z coordinates.
        :param position: 3D vector of the drone's position
        :param velocity: 3D vector of the drone's translation velocity
        :param velocity_ang: 3D vector of the drone's angular velocity
        :param acceleration: 3D vector of the drone's translation acceleration
        :param acceleration_ang: 3D vector of the drone's angular acceleration
        """
        return cls(position, velocity, velocity_ang, acceleration, acceleration_ang)
