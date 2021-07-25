"""
*Source Connector* defines a connection to a particular video source, which is given by particular class.

This file contains *File Connector* class which defines connection to video file.
"""

from __future__ import (
    annotations,
)  # allowing future references -> return class under which return value is returned
import typing
import numpy as np
from vidgear.gears import VideoGear
import cv2 as cv
from shared import param_validators as shared_param_val
from metron_conduit.miscellaneous import metron_conduit_param_validators as param_val
from .abstract_source import AbstractConnector


class FileConnector(AbstractConnector):
    """
    *File Connector* is a video file connector. It works as a context manager.

    Attributes:
        connector_type (str): String label for given *Source Connector* type.
        _file_path (str): Path to the file.
        _transcoding_resolution (typing.Tuple[int, int]): Input video file is trans-coded into the given resolution
            before it is streamed. Tuple representation is (transcoding_resolution_width,
            transcoding_resolution_height).
        _video_gear (vidgear.gears.VideoGear): Object holding a connection to the video file and
            able capture stream frames.
    """

    connector_type: typing.ClassVar[str] = "video_file"

    def __init__(self, file_path: str, transcoding_resolution: typing.Tuple[int, int]):
        """
        Stores all attributes needed to connect to the file.

        Args:
            file_path (str): Path to video file.
            transcoding_resolution (typing.Tuple[int, int]): Input video file is trans-coded into the given
                resolution before it is streamed. Tuple representation is
                (transcoding_resolution_width, transcoding_resolution_height).
        """
        shared_param_val.type_check(file_path, str)
        shared_param_val.type_check(transcoding_resolution[0], int)
        shared_param_val.type_check(transcoding_resolution[1], int)

        shared_param_val.file_existence_check(file_path)
        shared_param_val.resolution_validity_check(transcoding_resolution[0], transcoding_resolution[1])
        param_val.video_file_check(file_path)

        self._file_path = file_path
        self._transcoding_resolution = transcoding_resolution
        self._video_gear = VideoGear(source=self._file_path)

    def __enter__(self) -> FileConnector:
        """
        Context manager __entry__ method. Prepares VideoGear instance for frames reading.

        Returns (file_source.FileConnector): Itself.
        """
        self._video_gear.start()
        return self

    def __exit__(
        self,
        exc_type: typing.Optional[Exception],
        exc_val: typing.Optional[typing.Any],
        exc_tb: typing.Any,
    ) -> None:
        """
        Context manager __exit__ method. Stops VideoGear instance.

        Args:
            exc_type (typing.Optional[Exception]): Exception type.
            exc_val (typing.Optional[typing.Any]): Exception value.
            exc_tb (typing.Any): Exception traceback.

        Returns (None):
        """
        self._video_gear.stop()

    def get_frame(self) -> typing.Union[np.array]:
        """
        Returns next frame of the video source.

        Returns (typing.Union[np.array]): 3-dim array representing video frame in the order B, G, R.
            If obtained frame is `None`, which means video file stream is broken or finished, then `None` is returned.
        """
        frame = self._video_gear.read()
        if frame is None:
            return None

        return cv.resize(frame, dsize=self._transcoding_resolution)

    def get_stream_resolution(self) -> typing.Tuple[int, int]:
        """ "
        Returns stream transcoding resolution.

        Returns (typing.Tuple[int, int]): Resolution. Format [stream_width, stream_height].
        """
        return self._transcoding_resolution
