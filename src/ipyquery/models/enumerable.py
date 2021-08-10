class Enumerable():
    def __init__(self, iterable):
        self.__iterable = iterable

    def __get_elements(self):
        for x in self.__iterable:
            yield x

    def __iter__(self):
        return self.__get_elements()
