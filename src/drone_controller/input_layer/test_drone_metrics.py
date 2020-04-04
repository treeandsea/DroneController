from unittest import TestCase

from src.drone_controller.input_layer.drone_metrics import DroneMetrics


class DroneMetricTest(TestCase):
    def setUp(self) -> None:
        """
        Sets up some drone metrics.
        """

        self.mass = 2.56
        self.radius = 13.4
        self.rotor_count = 8
        self.thrust_per_rotor = 43.2

        self.metrics_dict = {'mass': self.mass,
                             'thrust_per_rotor': self.thrust_per_rotor,
                             'rotor_count': self.rotor_count,
                             'radius': self.radius}

        self.metrics = DroneMetrics(mass=self.mass,
                                    thrust_per_rotor=self.thrust_per_rotor,
                                    rotor_count=self.rotor_count,
                                    radius=self.radius)

    def test_metric_dict(self):
        """
        Test if the dictionary is correctly built.
        """

        self.assertEqual(self.metrics.metric_dict, self.metrics_dict)

    def test_metrics_from_dict(self):
        self.assertEqual(self.metrics, DroneMetrics())
