"""
This module provides data structures/patterns (classes or decorators).
"""


import typing
from types import MethodType


class Singleton:
    """
    Represents singleton data pattern applicable on class / function / method . When applied on a class,
    only one instance of the class is allowed for whole program lifespan. When applied on a function / method , only
    one call is allowed for whole program lifespan. The decorator can be applied on more classes / functions / methods,
    not only on one object of the program. It does not change decorated object.

    Attributes:
        _called (typing.Set[typing.Any]): Set data structure which keeps one use across classes / functions / methods.
        _function (typing.Any): Class / function / method on which the decorator is applied.
    """

    _called: typing.Set[typing.Any] = set()

    def __init__(self, decorated_object: typing.Any):
        """
        Saves decorated object as attribute, for later lookup.

        Args:
            decorated_object (typing.Any): Decorated object.
        """
        self._decorated_object = decorated_object

    def __call__(self, *args: typing.List[typing.Any], **kwargs: typing.Dict[str, typing.Any]) -> typing.Any:
        """
        It checks if decorated object was not already instantiated or called.
        If does not, it allows to create / call it. The method is called when decorator
        is applied on class / function / method.

        Args:
            *args (typing.List[typing.Any]): Positional arguments.
            **kwargs (typing.Dict[str, typing.Any]): Key-worded arguments.

        Returns (Typing.Any): Decorated object itself without change.

        Exceptions:
            Exception: Violence of singleton paradigm of decorated object.
        """
        if self._decorated_object not in self._called:
            self._called.add(self._decorated_object)
        else:
            raise Exception(
                f"Decorated {self._decorated_object} as `Singleton` can be called " f"/ instantiated only once!"
            )

        return self._decorated_object(*args, **kwargs)

    def __get__(self, instance: typing.Any, owner: typing.Any) -> typing.Any:
        """
        The method is needed to work with class method.

        Args:
            instance (typing.Any): Class instance.
            owner (typing.Any): Instance class owner.

        Returns (typing.Any):

        Exceptions:
            Exception: Violence of singleton paradigm of decorated object.
        """
        if instance is None:
            return self

        if owner not in self._called:
            self._called.add(owner)
        else:
            raise Exception(
                f"Decorated {self._decorated_object} as `Singleton` can be called " f"/ instantiated only once!"
            )

        return self.__class__(MethodType(self._decorated_object, instance))
