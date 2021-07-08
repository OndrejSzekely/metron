"""
This module provides decorator <create_structured_config_schema> which creates a *Structured Config Schema* used by
Hydra framework to validate presence of expected config parameters and their type. It calls schema registration
function passed as an argument into the function. The decorator has to be used before calling Hydra's <hydra.main>.
See the sample code:

```
@create_structured_config_schema(schema_registration_function_to_be_called)
@hydra.main(config_path="...", config_name="...")
@other_decorators
def main(cfg: DictConfig) -> None:
    ...
```
"""


import typing
from functools import wraps
from hydra.core.config_store import ConfigStore
from omegaconf import DictConfig


def create_structured_config_schema(
    schema_registering_function: typing.Callable[[ConfigStore], None]
) -> typing.Callable[[typing.Callable[..., DictConfig]], typing.Callable[..., DictConfig]]:
    """
    Creates *Structured Config Schema* of Hydra framework which is used to validate config parameters presence
    and data types. It does not validate config parameter values. The actual schema registering is done by
    <schema_registering_function> function. The advantage of decorator, rather than calling a function in main file,
    is code transparency from usage perspective.

    Args:
        schema_registering_function (typing.Callable[[ConfigStore]], None]): Function which does actual Structured
        Config Schema registration. The function has to have only one input parameter of type ConfigStore and return
        None.

    Returns (typing.Callable[[typing.Callable[..., typing.Any]], DictConfig]): Hydra's main decorator function.
    """

    def call_schema_register(hydra_main_func: typing.Callable[..., DictConfig]) -> typing.Callable[..., DictConfig]:
        """
        Calls <schema_registering_function> function at first and then returns decorated Hydra's main decorator
        function.

        Args:
            hydra_main_func (typing.Callable[..., typing.Any]): Hydra's main decorator function.

        Returns (typing.Callable[..., DictConfig]): Decorated Hydra's main decorator function.

        """
        config_store = ConfigStore.instance()
        schema_registering_function(config_store)

        @wraps(hydra_main_func)
        def hydra_main_decorator(*args: typing.List[typing.Any], **kwargs: typing.Dict[str, typing.Any]) -> DictConfig:
            """
            Decorator wrapped of Hydra's main function.

            Args:
                *args (typing.List[typing.Any]): Positional arguments.
                **kwargs (typing.Dict[str, typing.Any]): Key-worded arguments.

            Returns (DictConfig): Hydra's configuration.
            """

            return hydra_main_func(*args, **kwargs)

        return hydra_main_decorator

    return call_schema_register
