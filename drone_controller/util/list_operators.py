def add_lists(first_list, second_list):
    """
    Adds two lists element wise
    :param first_list:
    :param second_list:
    :return:
    """
    return [sum(x) for x in zip(first_list, second_list)]


def subtract_lists(first_list, second_list):
    """
    Subtracts two lists
    :param first_list:
    :param second_list:
    :return: one list
    """
    return [x - y for x, y in zip(first_list, second_list)]


def multiply_lists(first_list, second_list):
    """
    Multiplies two lists element wise
    :param first_list:
    :param second_list:
    :return:
    """
    return [a * b for a, b in zip(first_list, second_list)]
