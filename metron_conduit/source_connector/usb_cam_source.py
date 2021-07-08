"""
`Source Connector` defines a connection to a particular video source, which is given by particular class.

This file contains `USB Cam Connector` class, with a helper class, which defines connection to USB cam.
"""

from __future__ import (
    annotations,
)  # allowing future references -> return class under which return value is returned
import typing
from dataclasses import dataclass
import json
import numpy as np
from vidgear.gears import VideoGear
import cv2 as cv
from metron_conduit.miscellaneous import metron_conduit_param_validators as param_val
from shared import param_validators as shared_param_val
from .abstract_source import AbstractConnector

_TIME_DELAY_VALID_UPPER_BOUND: typing.Final[int] = 2 * 60  # in seconds


@dataclass
class _CamOptions:
    """
    Defines camera options used by underlying OpenCV VideoCapture API which is called by CamGear in `USB Cam Connector`.
    Attribute names correspond to OpenCV VideoCapture API options, except lowercase.

    Attributes:
        cap_prop_frame_width (int): Camera frame width. Could be lower than native camera resolution.
        cap_prop_frame_height (int): Camera frame height. Could be lower than native camera resolution.
        cap_prop_fps (int): FPS of the stream. Has to be supported by the camera.
        cap_prop_brightness (int): Camera brightness level. Currently is not supported on MacOS.
        cap_prop_contrast (int): Camera contrast level. Currently is not supported on MacOS.
        cap_prop_saturation (int): Camera saturation level. Currently is not supported on MacOS.
        cap_prop_hue (int): Camera hue level. Currently is not supported on MacOS.
        cap_prop_zoom (int): Camera zoom level. Currently is not supported on MacOS.
        cap_prop_focus (int): Camera focus level. Currently is not supported on MacOS.
        cap_prop_autofocus (int): Enable or disable camera autofocus. Currently is not supported on MacOS.
        cap_prop_auto_wb (int): Camera auto white balancing level. Currently is not supported on MacOS.
    """

    # pylint: disable=too-many-instance-attributes
    # higher number of attributes is reasonable in this case

    cap_prop_frame_width: int
    cap_prop_frame_height: int
    cap_prop_fps: int
    cap_prop_brightness: typing.Optional[int]
    cap_prop_contrast: typing.Optional[int]
    cap_prop_saturation: typing.Optional[int]
    cap_prop_hue: typing.Optional[int]
    cap_prop_zoom: typing.Optional[int]
    cap_prop_focus: typing.Optional[int]
    cap_prop_autofocus: typing.Optional[int]
    cap_prop_auto_wb: typing.Optional[int]

    def get_kw_options(self) -> dict:
        """
        Converts options as class attributes into JSON with uppercase for keys. This is
        required by VidGear which consumes the dictionary. If option value is equal None, then the option is discarded
        from output key-worded JSON, because camera default value should be used for the option.

        Returns (dict): Instance attributes converted into dictionary with uppercase for keys.
        """
        kw_options = json.loads(json.dumps(self.__dict__))
        kw_options_uppercase = {key.upper(): value for key, value in kw_options.items() if value is not None}
        return kw_options_uppercase


class UsbCamConnector(AbstractConnector):
    """
    `USB Cam Connector` is an USB cam connector. It works as a context manager.

    Attributes:
        connector_type (str): String label for given `Source Connector` type.
        _camera_id (int): Camera id.
        _time_delay (int): Time delay in seconds, before camera starts to stream. Default value is `0`.
        _camera_option (usb_cam_source._CamOptions): Camera options setup used by underlying OpenCV VideoCapture API
            in NetGear.
        _video_gear (vidgear.gears.VideoGear): Object holding a connection to the camera and
            able capturecamera stream. Instantiated VideoGear is assigned when entering into context and
            on close set to None.
    """

    connector_type: typing.ClassVar[str] = "usb_camera"

    def __init__(
        self,
        camera_id: int,
        cam_frame_res: typing.Tuple[int, int],
        cam_fps: int,
        cam_brightness: typing.Optional[int] = None,
        cam_contrast: typing.Optional[int] = None,
        cam_saturation: typing.Optional[int] = None,
        cam_hue: typing.Optional[int] = None,
        cam_zoom: typing.Optional[int] = None,
        cam_focus: typing.Optional[int] = None,
        cam_autofocus: typing.Optional[int] = None,
        cam_auto_wb: typing.Optional[int] = None,
        time_delay: int = 0,
    ):
        """
        Stores all attributes needed to connect to the camera.

        Args:
            camera_id (int): Camera device id.
            cam_frame_res (Tuple[int, int]): Camera frame resolution. Could be lower than native camera resolution.
                Tuple representation is (frame_resolution_width, frame_resolution_height).
            cam_fps (int): FPS of the stream. Has to be supported by the camera.
            cam_brightness (typing.Optional[int]): Camera brightness level. Currently is not supported on MacOS.
            cam_contrast (typing.Optional[int]): Camera contrast level. Currently is not supported on MacOS.
            cam_saturation (typing.Optional[int]): Camera saturation level. Currently is not supported on MacOS.
            cam_hue (typing.Optional[int]): Camera hue level. Currently is not supported on MacOS.
            cam_zoom (typing.Optional[int]): Camera zoom level. Currently is not supported on MacOS.
            cam_focus (typing.Optional[int]): Camera focus level. Currently is not supported on MacOS.
            cam_autofocus (typing.Optional[int]): Enable or disable camera autofocus. Currently is not supported
                on MacOS.
            cam_auto_wb (typing.Optional[int]): Camera auto white balancing level. Currently is not supported
                on MacOS.
            time_delay (typing.Optional[int]): Time delay in seconds, before camera starts to stream.
                Value greater than 0 is beneficial for camera warm-up.
        """

        # pylint: disable=too-many-arguments
        # Most of the arguments are None by default, so not all parameters are needed to specify and encapsulation in
        # more classes would make instantiating process more complicated, because Hydra instantiate feature is used.

        shared_param_val.type_check(camera_id, int)
        shared_param_val.type_check(cam_frame_res[0], int)
        shared_param_val.type_check(cam_frame_res[1], int)
        shared_param_val.type_check(cam_fps, int)
        shared_param_val.type_check(cam_brightness, (int, type(None)))
        shared_param_val.type_check(cam_contrast, (int, type(None)))
        shared_param_val.type_check(cam_saturation, (int, type(None)))
        shared_param_val.type_check(cam_hue, (int, type(None)))
        shared_param_val.type_check(cam_zoom, (int, type(None)))
        shared_param_val.type_check(cam_focus, (int, type(None)))
        shared_param_val.type_check(cam_autofocus, (int, type(None)))
        shared_param_val.type_check(cam_auto_wb, (int, type(None)))
        shared_param_val.type_check(time_delay, int)

        param_val.cam_device_existence_check(camera_id)
        shared_param_val.resolution_validity_check(cam_frame_res[0], cam_frame_res[1])
        param_val.cam_resolution_support_check(camera_id, cam_frame_res)
        param_val.cam_fps_support_check(camera_id, cam_fps)
        if cam_brightness is not None:
            param_val.cam_control_support_check(camera_id, "brightness", cv.CAP_PROP_BRIGHTNESS, cam_brightness)
        if cam_contrast is not None:
            param_val.cam_control_support_check(camera_id, "contrast", cv.CAP_PROP_CONTRAST, cam_contrast)
        if cam_saturation is not None:
            param_val.cam_control_support_check(camera_id, "saturation", cv.CAP_PROP_SATURATION, cam_saturation)
        if cam_hue is not None:
            param_val.cam_control_support_check(camera_id, "hue", cv.CAP_PROP_HUE, cam_hue)
        if cam_zoom is not None:
            param_val.cam_control_support_check(camera_id, "zoom", cv.CAP_PROP_ZOOM, cam_zoom, -100, 100)
        if cam_focus is not None:
            param_val.cam_control_support_check(camera_id, "focus", cv.CAP_PROP_FOCUS, cam_focus, 0, 255)
        if cam_autofocus is not None:
            param_val.cam_control_support_check(camera_id, "autofocus", cv.CAP_PROP_AUTOFOCUS, cam_autofocus, 0, 1)
        if cam_auto_wb is not None:
            param_val.cam_control_support_check(camera_id, "auto white balance", cv.CAP_PROP_AUTO_WB, cam_auto_wb, 0, 1)
        shared_param_val.parameter_value_in_range(time_delay, 0, _TIME_DELAY_VALID_UPPER_BOUND)

        self._camera_id = camera_id
        self._time_delay = time_delay
        self._camera_option = _CamOptions(
            cap_prop_frame_width=cam_frame_res[0],
            cap_prop_frame_height=cam_frame_res[1],
            cap_prop_fps=cam_fps,
            cap_prop_brightness=cam_brightness,
            cap_prop_contrast=cam_contrast,
            cap_prop_saturation=cam_saturation,
            cap_prop_hue=cam_hue,
            cap_prop_zoom=cam_zoom,
            cap_prop_focus=cam_focus,
            cap_prop_autofocus=cam_autofocus,
            cap_prop_auto_wb=cam_auto_wb,
        )
        self._video_gear = VideoGear(
            source=self._camera_id, time_delay=self._time_delay, **self._camera_option.get_kw_options()
        )

    def __enter__(self) -> UsbCamConnector:
        """
        Context manager __entry__ method. Prepares VideoGear instance for frames reading.

        Returns (usb_cam_source.UsbCamConnector): Itself.
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
        Context manager __exit__ method. Stops VideoGear instance and clears the attribute.

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
            If camera stream is broken and obtained frame is `None`, then `None` is returned.
        """
        frame = self._video_gear.read()

        return frame

    def get_stream_resolution(self) -> typing.Tuple[int, int]:
        """ "
        Returns set USB cam resolution.

        Returns (typing.Tuple[int, int]): Resolution. Format [stream_width, stream_height].
        """
        return self._camera_option.cap_prop_frame_width, self._camera_option.cap_prop_frame_height
