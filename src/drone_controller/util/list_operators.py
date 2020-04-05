def subtract_lists(first_list, second_list):
    """
    Subtracts two lists
    :param first_list:
    :param second_list:
    :return: one list
    """
    return [x - y for x, y in zip(first_list, second_list)]
