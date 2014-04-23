__author__ = 'vdsq3226'

LIST_PDP = {}


def get_pdp(name):
    """
    Search for an instance of PDP or create it.
    """
    if name in LIST_PDP:
        return LIST_PDP[name]
    else:
        pdp = create_pdp(name)
        return pdp


class PDP:
    # TODO: create the class
    def __init__(self):
        pass


def create_pdp(name):
    """
    Create an instance of PDP.
    """
    # TODO: create the instance
    pass