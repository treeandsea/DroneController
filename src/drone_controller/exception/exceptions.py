class DroneControllerError(Exception):
    """
    Base class for exception in this module.
    """


class UserInputError(DroneControllerError):
    """
    Incorrect user input.
    """

    def __init__(self, expression, message):
        super().__init__()
        self.expression = expression
        self.message = message
