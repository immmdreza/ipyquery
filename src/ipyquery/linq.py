from collections.abc import Iterable
from typing import Callable, Any, Dict


class Linq:
    """
    `Language integrated query` for Python

    """
    def __init__(self, iterable: Iterable):
        try:
            if isinstance(iterable, dict):
                self.__generator = iterable.items()
            else:
                self.__generator = list(iterable)
        except TypeError:
            raise

    @staticmethod
    def __check_operation(operation: Callable[[Any], Any], value):
        if operation is None:
            return True
        else:
            return operation(value)

    def __len__(self):
        return len(self.__generator)

    def __iter__(self):
        return (x for x in self.__generator)

    def select(self, key: Callable[[Any], Any]):
        """Projects each element of a sequence into a new form.

        Parameters
        ----------
        key : `Callable[[Any], Any]`
            Callable to be called on each element of the sequence.
        """

        if key is None:
            raise ValueError("key must not be None")

        self.__generator = list(map(key, self.__generator))
        return self

    def select_many(self, key: Callable[[Any], Iterable[Any]] = None):
        """Projects each element of a sequence to an `Iterable[Any]`
        and flattens the resulting sequences into one sequence.

        Parameters
        ----------
        key : `Callable[[Any], Iterable[Any]]`
            Callable to be called on each element of the sequence.
        """

        result = []
        should_check = key is not None
        for x in self.__generator:
            if not should_check:
                value = x
            else:
                value = key(x)

            try:
                for inner in value:
                    result.append(inner)
            except TypeError:
                raise Exception("Selected item should be Iterable")
        self.__generator = result
        return self

    def enum_select(self, key: Callable[[int, Any], Any] = None):
        should_check = key is not None

        self.__generator = [
            key(i, x) if should_check else (i, x)
            for i, x in enumerate(self.__generator)
        ]
        return self

    def tolist(self):
        if isinstance(self.__generator, dict):
            return [(x, self.__generator[x]) for x in self.__generator]

        return list(self.__generator)

    def todict(self,
               key_selector: Callable[[Any], Any],
               value_selector: Callable[[Any], Any] = None):
        should_check_value = value_selector is not None
        result = {}
        for x in self.__generator:
            key = key_selector(x)
            if key not in result:
                if isinstance(self.__generator, dict):
                    x = self.__generator[key]

                if should_check_value:
                    value = value_selector(x)
                else:
                    value = x

                result[key] = value
        return result

    def groupby(self,
                key_selector: Callable[[Any], Any],
                comparer: Callable[[Any, Any], bool] = None,
                value_selector: Callable[[Any], Any] = None):
        if comparer is None:
            comparer = lambda x, y: x == y
        should_check_value = value_selector is not None
        result: Dict[Any, list[Any]] = {}
        for x in self.__generator:
            key = key_selector(x)

            is_new = True
            for r in result:
                if comparer(r, key):
                    is_new = False
                    break

            if should_check_value:
                value = value_selector(x)
            else:
                value = x

            if not is_new:
                result[key].append(value)
            else:
                result[key] = [value]
        self.__generator = result.items()
        return self

    def where(self, operation: Callable[[Any], bool]):
        if operation is None:
            raise ValueError("Where what? fill parameters.")

        self.__generator = list(filter(operation, self.__generator))
        return self

    def element_at(self, index):
        return self.__generator[index]

    def first(self, operation: Callable[[Any], bool] = lambda _: True):
        return self.where(operation).element_at(0)

    def first_or_default(self,
                         operation: Callable[[Any], bool] = lambda _: True,
                         default=None):
        for x in self.where(operation):
            return x
        return default

    def any(self, operation: Callable[[Any], bool] = lambda _: True):
        return any([operation(x) for x in self.__generator])

    def all(self, operation: Callable[[Any], bool] = None):
        if operation is None:
            raise ValueError('operation is required')

        return all([operation(x) for x in self.__generator])

    def orderby(self, key: Callable[[Any], None] = None):
        self.__generator = sorted(self.__generator, key=key)
        return self

    def orderby_desc(self, key: Callable[[Any], None] = None):
        self.__generator = sorted(self.__generator, key=key, reverse=True)
        return self

    def max(self, key: Callable[[Any], None] = None) -> Any:
        return max(self.__generator, key=key)

    def min(self, key: Callable[[Any], None] = None) -> Any:
        return min(self.__generator, key=key)

    def sum(self, key: Callable[[Any], None] = lambda _: _) -> int:
        return sum(map(key, self.__generator))

    def average(self, key: Callable[[Any], None] = lambda _: _):
        sum = self.sum(key)
        return sum / len(self)

    def distinct(self, key: Callable[[Any], None] = None):
        result = []
        should_check = key is not None
        for x in self.__generator:
            if not should_check:
                if x not in result:
                    result.append(x)
            else:
                value = key(x)
                should_append = True
                for r in result:
                    if key(r) == value:
                        should_append = False
                        break
                if should_append:
                    result.append(x)
        self.__generator = result
        return self

    def single(self, operation: Callable[[Any], bool] = lambda _: True):
        result = self.where(operation)
        l = len(result)
        if l == 1:
            return result.first()
        elif l == 0:
            raise Exception("Sequence has no elements")
        else:
            raise Exception("Sequence has more that one elements")

    def single_or_default(self,
                          operation: Callable[[Any], bool] = lambda _: True,
                          default=None):
        result = self.where(operation)
        l = len(result)
        if l == 1:
            return result.first()
        else:
            return default

    def add(self, item: Any):
        self.__generator.append(item)
        return self

    def reverse(self):
        self.__generator.reverse()
        return self

    def remove_all(self, operation: Callable[[Any], bool] = None):
        if operation is None:
            self.__generator.clear()

        result = []
        for x in self.__generator:
            if operation(x):
                continue
            else:
                result.append(x)
        self.__generator = result
        return self

    def remove(self, item: Any):
        self.__generator.remove(item)
        return self

    def skip(self, count: int):
        self.__generator = self.__generator[count:]
        return self

    def take(self, count: int):
        self.__generator = self.__generator[:count]
        return self
