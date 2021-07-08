"""
This module defines variable <config> which stores configuration of given Metron's component obtained by Hydra
framework.

<config> has to be initialized by using provided function decorator <set_hydra_config>,
which has to be used right after Hydra's <hydra.main> decorator. See the sample code:

```
@hydra.main(config_path="...", config_name="...")
@set_hydra_config
def main(cfg: DictConfig) -> None:
```

<config> is obtained by using provided function / class method decorated <GetHydraConfig>, which passes Hydra's config
as the first argument. See the sample code:

```
@GetHydraConfig
def do_something(hydra_config: DictConfig):
    ...
```
"""

import typing
from functools import wraps
from types import MethodType
from omegaconf import DictConfig, OmegaConf
from shared.structures import Singleton


config = None  # pylint: disable=invalid-name


@Singleton
def set_hydra_config(main_function: typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]:
    """
    Decorator used to initializes global <config> variable with Hydra's config. The decorator has to be be called once,
    right after the Hydra's decorator <hydra.main>.

    Args:
        main_function (typing.Callable[..., typing.Any]): Main script function which performs program orchestration.

    Returns (typing.Callable[..., typing.Any]): Decorated main_function.
    """

    @wraps(main_function)
    def decorated_function(cfg: DictConfig) -> DictConfig:
        """
        Decorating function which initializes global <config> variable with Hydra's configuration.

        Args:
            cfg (DictConfig): Hydra's configuration.

        Returns (DictConfig): Hydra's configuration.
        """
        global config  # pylint: disable=global-statement, invalid-name
        OmegaConf.set_readonly(cfg, True)
        config = cfg

        return main_function(cfg)

    return decorated_function


class GetHydraConfig:
    """
    Decorator used to get global <config> variable storing Hydra's config. The decorated might be applied on a function
    or a class method. It passes into decorated function / method the config as the first argument.

    Attributes:
        _decorated_func (typing.Any): Function / method on which the decorator is applied.
    """

    def __init__(self, decorated_func: typing.Any):
        """
        Saves decorated function / method as attribute, for later lookup.

        Args:
            decorated_func (typing.Any): Decorated function / method.
        """
        self._decorated_func = decorated_func

    def __call__(
        self, *args: typing.List[typing.Any], **kwargs: typing.Dict[str, typing.Any]
    ) -> typing.Callable[..., typing.Any]:
        """
        Passes Hydra's config, stored in <config> global variable, as a first argument of the function / method.
        The method is called when decorator is applied on class method or function.

        Args:
            *args (typing.List[typing.Any]): Positional arguments.
            **kwargs (typing.Dict[str, typing.Any]): Key-worded arguments.

        Returns (typing.Callable[..., typing.Any]): Decorated function which takes Hydra's config as the
            first input argument.
        """
        global config  # pylint: disable=global-statement, invalid-name
        return self._decorated_func(config, *args, **kwargs)

    def __get__(self, instance: typing.Any, owner: typing.Any) -> typing.Any:
        """
        The method is needed to work with class method.

        Args:
            instance (typing.Any): Class instance.
            owner (typing.Any): Instance class owner.

        Returns (typing.Any):
        """
        return self.__class__(MethodType(self._decorated_func, instance))
