"""
*Video Streamer* sends out video stream, obtained by particular *Source Connector*, to other Metron components.

This file contains *Streamer Worker* class which performs streaming job with given configuration.
"""

from __future__ import (
    annotations,
)  # allowing future references -> return class under which return value is returned
import typing
import logging
import asyncio
import cv2 as cv
import numpy as np
from vidgear.gears.asyncio import NetGear_Async
from metron_conduit.source_connector.abstract_source import AbstractConnector
from shared import param_validators as shared_param_val
from shared import metron_globals


class StreamerWorker:
    """
    *Streamer Worker* does the streaming job with the given configuration. It receives video stream frames, one by one,
    and dispatch them to other Metron's components. It works as a context manager.

    Attributes:
        _address (str): IP address of the server.
        _port (str): Stream port.
        _com_protocol (str): Protocol used for streaming communication.
        _com_pattern (int): Communication pattern used for streaming.
        _stream_fps (float): FPS of the stream. Can be non-integer and even less than one. This is possible because
                FPS is translated into stream frame latency is seconds.
        _stream_frame_res (Tuple[int, int]): Stream frame resolution. Could be lower or higher than native input
                resolution. Tuple representation is (frame_resolution_width, frame_resolution_height).
        _debug_logging (bool): Activate/deactivate debug logging of NetGear
        _net_gear_streamer (vidgear.gears.asyncio.NetGear_Async): Object responsible for streaming.
            Instantiated NetGear is assigned when entering into context and on close set to None.
    """

    # pylint: disable=too-many-instance-attributes
    # 8/7 attributes is acceptable in this case.

    SUPPORTED_COM_PROTOCOLS: typing.Final[typing.List[str]] = ["tcp", "ipc"]
    SUPPORTED_COM_PATTERNS: typing.Final[typing.List[int]] = [
        0,
        1,
        2,
        3,
    ]  # zmq.PAIRV, zmq.REQ/zmq.REPV, zmq.PUB/zmq.SUB, zmq.PUSH/zmq.PULL
    SUPPORTED_MAX_STREAM_FPS: typing.Final[float] = 60.0
    SUPPORTED_MIN_STREAM_FPS: typing.Final[float] = 1e-2

    def __init__(
        self,
        address: str,
        port: str,
        com_protocol: str,
        com_pattern: int,
        stream_frame_res: typing.Tuple[int, int],
        stream_fps: float,
    ):
        """
        Stores all attributes needed to broadcast the stream.

        Args:
            address (str): IP address of the server.
            port (typing.List[str]): List of ports on which the streams are provided. One port per one client.
            com_protocol (str): Protocol used for streaming communication.
            com_pattern (int): Communication pattern used for streaming.
            stream_frame_res (Tuple[int, int]): Stream frame resolution. Could be lower or higher than native input
                resolution. Tuple representation is (frame_resolution_width, frame_resolution_height).
            stream_fps (float): FPS of the stream. Can be non-integer and even less than one. This is possible because
                FPS is translated into stream frame latency is seconds.
        """

        # pylint: disable=too-many-arguments
        # Encapsulation in more classes would make instantiating process more complicated,
        # because Hydra instantiate feature is used.

        shared_param_val.type_check(address, str)
        shared_param_val.type_check(port, str)
        shared_param_val.type_check(com_protocol, str)
        shared_param_val.type_check(com_pattern, int)
        shared_param_val.type_check(stream_frame_res[0], int)
        shared_param_val.type_check(stream_frame_res[1], int)
        shared_param_val.type_check(stream_fps, float)

        shared_param_val.resolution_validity_check(stream_frame_res[0], stream_frame_res[1])
        shared_param_val.parameter_value_in_range(
            stream_fps, self.SUPPORTED_MIN_STREAM_FPS, self.SUPPORTED_MAX_STREAM_FPS
        )
        com_protocol = com_protocol.lower()
        if com_protocol not in self.SUPPORTED_COM_PROTOCOLS:
            raise ValueError(
                f'Given <com_protocol> value "{com_protocol}" is not supported. List of supported protocols: '
                f"{self.SUPPORTED_COM_PROTOCOLS}"
            )

        if com_pattern not in self.SUPPORTED_COM_PATTERNS:
            raise ValueError(
                f'Given <com_pattern> value "{com_pattern}" is not supported. List of '
                f"supported patterns: {self.SUPPORTED_COM_PATTERNS}"
            )

        self._address = address
        self._port = port
        self._com_protocol = com_protocol
        self._com_pattern = com_pattern
        self._stream_fps = stream_fps
        self._stream_frame_res = stream_frame_res
        self._debug_logging = bool(logging.getLogger().getEffectiveLevel() == logging.DEBUG)
        self._net_gear_streamer = NetGear_Async(
            address=self._address,
            port=self._port,
            protocol=self._com_protocol,
            pattern=self._com_pattern,
            logging=self._debug_logging,
        )
        self._net_gear_streamer.loop = metron_globals.event_loop

    def __enter__(self) -> StreamerWorker:
        """
        Context manager __entry__ method. Starts the streaming engine.

        Returns (StreamerWorker): Itself.
        """
        self._net_gear_streamer.launch()

        return self

    def __exit__(
        self,
        exc_type: typing.Optional[Exception],
        exc_val: typing.Optional[typing.Any],
        exc_tb: typing.Any,
    ) -> None:
        """
        Context manager __exit__ method. Stops NetGear.

        Args:
            exc_type (typing.Optional[Exception]): Exception type.
            exc_val (typing.Optional[typing.Any]): Exception value.
            exc_tb (typing.Any): Exception traceback.

        Returns (None):
        """
        self._net_gear_streamer.close()

    def get_streaming_task(self) -> asyncio.Task:
        """
        Returns task of async NetGear.

        Returns (asyncio.Task): Task of async NetGear.
        """
        return self._net_gear_streamer.task

    def set_frame_generator(self, source_connector: AbstractConnector) -> None:
        """
        Sets frame generator to async NetGear.

        Args:
            source_connector (AbstractConnector): *Source Connector* which provides source stream resolution.

        Returns (None):
        """
        shared_param_val.type_check(source_connector, AbstractConnector)

        src_res = source_connector.get_stream_resolution()

        # define resizing function used by <_frame_generator()> based on resolution
        if src_res == self._stream_frame_res:

            def resizing_func(img: np.array) -> np.array:
                return img

        else:

            def resizing_func(img: np.array) -> np.array:
                return cv.resize(img, self._stream_frame_res)

        async def _frame_generator() -> typing.AsyncGenerator:
            video_source = source_connector
            frame_latency = 1.0 / self._stream_fps

            has_frame = True
            while has_frame is not None:
                frame = video_source.get_frame()

                if frame is not None:
                    resized_frame = resizing_func(frame)
                    yield resized_frame

                    await asyncio.sleep(frame_latency)
                else:
                    has_frame = False

        self._net_gear_streamer.config["generator"] = _frame_generator()
