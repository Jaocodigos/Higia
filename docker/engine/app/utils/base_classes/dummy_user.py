

class DummyUser:

    def __init__(self, **kwargs):
        self._dict = kwargs
        self.__dict__.update(kwargs)
