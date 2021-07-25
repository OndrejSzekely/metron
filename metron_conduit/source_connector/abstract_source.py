"""
*Source Connector* defines a connection to a particular video source, which is given by particular class.

This file contains *Abstract Connector* class which defines common interface across all *Source Connector* types.
"""

from __future__ import (
    annotations,
)  # allowing future references -> return class under which return value is returned
from abc import ABC, abstractmethod
import typing
import numpy as np


class AbstractConnector(ABC):
    """
    *Abstract Connector* is an abstract class for any instantiable *Source Connectors*. It works as a context manager.

    Attributes:
        connector_type (str): String label for given *Source Connector* type.
    """

    @property
    def connector_type(self) -> str:
        """
        Defines attribute `connector_type` using "get" method as not implemented - abstract attribute.

        Returns (str):
        """
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> AbstractConnector:
        """
        Context manager __entry__ method.

        Returns (abstract_source.AbstractConnector): Itself.
        """

    @abstractmethod
    def __exit__(
        self,
        exc_type: typing.Optional[Exception],
        exc_val: typing.Optional[typing.Any],
        exc_tb: typing.Any,
    ) -> None:
        """
        Context manager __exit__ method.

        Args:
            exc_type (typing.Optional[Exception]): Exception type.
            exc_val (typing.Optional[typing.Any]): Exception value.
            exc_tb (typing.Any): Exception traceback.

        Returns (None):
        """

    @abstractmethod
    def get_frame(self) -> typing.Union[np.array]:
        """
        Returns next frame of the video source.

        Returns (numpy.array): 3-dim array representing video frame in the order B,G,R.
            If camera stream is broken and obtained frame is `None`, then `None` is returned.
        """

    @abstractmethod
    def get_stream_resolution(self) -> typing.Tuple[int, int]:
        """
        Returns output source stream resolution.

        Returns (typing.Tuple[int, int]): Output source resolution. Format [stream_width, stream_height].
        """
