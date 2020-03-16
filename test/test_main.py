"""
Tests the main welcome function.
"""
import src.drone_controller.main


def test_welcome(capsys):
    """
    This tests the main method if it prints the welcome message.
    This test is more a workflow test than a real code test.
    :param capsys: caputed output in out and error
    """
    src.drone_controller.main.welcome()
    captured = capsys.readouterr()
    expected_out = 'Welcome to DroneController. Enjoy your flight.\n'
    assert captured.out == expected_out
