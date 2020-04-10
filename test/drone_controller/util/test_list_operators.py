from drone_controller.util.list_operators import add_lists, subtract_lists, multiply_lists

FIRST = [1, 2, 3]
SECOND = [4, 5, 6]


def test_add_lists():
    """
    Tests list addition
    """
    expected = [5, 7, 9]
    assert expected == add_lists(FIRST, SECOND)


def test_subtract_lists():
    """
    Tests list subtraction
    """
    expected = [3, 3, 3]
    assert expected == subtract_lists(SECOND, FIRST)


def test_multiply_lists():
    """
    Tests the lists multiplies.
    """
    expected = [4, 10, 18]
    assert expected == multiply_lists(FIRST, SECOND)
