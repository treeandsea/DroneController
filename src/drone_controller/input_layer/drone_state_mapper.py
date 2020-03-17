"""
Mapper Module
"""


class DroneStateMapper:
    """
    Maps different inputs to an expected drone state.
    """

    def keyboard(self, user_input):
        """
        Maps keyboard input.
        :param user_input: four rotation keys and one for acceleration
        """
        raise NotImplementedError
