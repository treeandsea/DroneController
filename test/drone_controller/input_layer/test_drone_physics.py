from unittest import TestCase

from drone_controller.input_layer.drone_physics import DronePhysics


class DronePhysicsTest(TestCase):
    """
    Tests the wrapper class DronePhysics.
    """

    def setUp(self) -> None:
        """
        Sets up some drone physics.
        """

        self.mass = 2.56
        self.radius = 13.4
        self.rotor_count = 8
        self.thrust_per_rotor = 43.2

        self.physics_dict = {'mass': self.mass,
                             'thrust_per_rotor': self.thrust_per_rotor,
                             'rotor_count': self.rotor_count,
                             'radius': self.radius}

        self.physics = DronePhysics(mass=self.mass,
                                    thrust_per_rotor=self.thrust_per_rotor,
                                    rotor_count=self.rotor_count,
                                    radius=self.radius)

    def test_physics_dict(self):
        """
        Test if the dictionary is correctly built.
        """

        self.assertEqual(self.physics.physics_dict(), self.physics_dict)

    def test_physics_from_dict(self):
        """
        Tests if drone physics is correctly built from dict.
        """
        self.assertEqual(self.physics, DronePhysics(**self.physics_dict))

    def test_not_equal(self):
        """
        Tests the eq method for inequality.
        """
        physics_dict = self.physics_dict
        physics_dict['mass'] = 5

        other_physics = DronePhysics(**physics_dict)

        self.assertNotEqual(self.physics, other_physics)

    def test_wrong_type(self):
        """
        Tests if type checking works.
        """
        with self.assertRaises(TypeError):
            self.physics.__eq__(10)
