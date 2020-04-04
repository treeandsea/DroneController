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

        self.metrics = DroneMetrics(self.mass, self.thrust_per_rotor, self.rotor_count, self.radius)

    def test_metric_dict(self):
        """
        Test if the dictionary is correctly built.
        """
        metrics_dict = {'mass': self.mass,
                        'thrust_per_rotor': self.thrust_per_rotor,
                        'rotor_count': self.rotor_count,
                        'radius': self.radius}

        self.assertEqual(self.metrics.metric_dict, metrics_dict)
