"""
The module provides parameter validation functions specific for Metron Conduit. The scope of validation is all
parameters.
"""

import typing
import cv2 as cv
from pymediainfo import MediaInfo
from shared import custom_exception
from shared import param_validators as shared_param_val


_CV_CAP_OPTION_LOWER_BOUND: typing.Final[int] = 0
_CV_CAP_OPTION_UPPER_BOUND: typing.Final[int] = 100
_CAM_FPS_DIFF_EPS: typing.Final[float] = 1e-1


def cam_device_existence_check(camera_id: int) -> None:
    """
    Checks if camera given by <camera_id> is accessible. If not, an exception is raised.

    Args:
        camera_id (int): Checked camera id.

    Returns (None):

    Exceptions:
        IOCamDevError: If camera is not accessible.
    """
    shared_param_val.type_check(camera_id, int)

    cap = cv.VideoCapture(camera_id)
    if cap is None or not cap.isOpened():
        raise custom_exception.IOCamDevError(accessed_cam_id=camera_id)


def cam_resolution_support_check(camera_id: int, resolution: typing.Tuple[int, int]) -> None:
    """
    Checks if camera supports requested video stream resolution.

    Args:
        camera_id (int): Checked camera id.
        resolution (typing.Tuple[int, int]): Requested video stream resolution. Format [stream_width, stream_height].

    Returns (None):

    Exceptions:
        ValueError: If camera does not support requested stream resolution.
    """
    shared_param_val.type_check(camera_id, int)
    shared_param_val.type_check(resolution[0], int)
    shared_param_val.type_check(resolution[1], int)

    cap = cv.VideoCapture(camera_id)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, resolution[1])
    set_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    set_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
    if set_width != resolution[0] or set_height != resolution[1]:
        raise ValueError(
            f"Given resolution `{resolution}` is not supported by the camera. "
            f"Closest supported resolution is `[{set_width}, {set_height}]`"
        )


def cam_fps_support_check(camera_id: int, fps: int) -> None:
    """
    Checks if camera supports given video stream frame rate. The actual frame rate can vary a little (below O.),
    therefore we check if the given and the set FPS difference if below epsilon.

    Args:
        camera_id (int): Checked camera id.
        fps (int): Framerate.

    Returns (None):

    Exceptions:
        ValueError: If camera does not support requested framerate.
    """
    shared_param_val.type_check(camera_id, int)
    shared_param_val.type_check(fps, int)

    if fps <= 0 or fps > 60:
        raise ValueError(f"Given FPS `{fps}` is out of FPS reasonable range: (0, 60>.")

    cap = cv.VideoCapture(camera_id)
    cap.set(cv.CAP_PROP_FPS, fps)
    set_fps = cap.get(cv.CAP_PROP_FPS)
    if abs(set_fps - fps) > _CAM_FPS_DIFF_EPS:
        raise ValueError(f"Given FPS `{fps}` if not supported by the camera.")


def cam_control_support_check(
    camera_id: int,
    control_option_label: str,
    cam_cap_attribute: int,
    value: int,
    cam_option_lower_bound: typing.Optional[int] = None,
    cam_option_upper_bound: typing.Optional[int] = None,
) -> None:
    """
    Checks if camera supports given control attribute and particular value.

    Args:
        camera_id (int): Checked camera id.
        control_option_label (str): String label of camera control option for error logging purpose.
        cam_cap_attribute (int): OpenCV camera control attribute id.
        value (int): Camera control attribute value.
        cam_option_lower_bound (int): Lower bound for camera option validation.
        cam_option_upper_bound (int): Upper bound for camera option validation.

    Returns (None):

    Exceptions:
        ValueError: If camera does not support control attribute control nor requested control attribute level.
    """

    # pylint: disable=too-many-arguments
    # Additional one more parameter is acceptable.

    shared_param_val.type_check(camera_id, int)
    shared_param_val.type_check(control_option_label, str)
    shared_param_val.type_check(cam_cap_attribute, int)
    shared_param_val.type_check(value, int)
    shared_param_val.type_check(cam_option_lower_bound, (int, type(None)))
    shared_param_val.type_check(cam_option_upper_bound, (int, type(None)))

    cam_option_lower_bound = cam_option_lower_bound or _CV_CAP_OPTION_LOWER_BOUND
    cam_option_upper_bound = cam_option_upper_bound or _CV_CAP_OPTION_UPPER_BOUND

    try:
        shared_param_val.parameter_value_in_range(value, cam_option_lower_bound, cam_option_upper_bound)
    except ValueError as value_error:
        raise ValueError(
            f"Given {control_option_label} level `{value}` is out of the allowed range"
            f" <{cam_option_lower_bound}, {cam_option_upper_bound}>"
        ) from value_error

    cap = cv.VideoCapture(camera_id)
    cap.set(cam_cap_attribute, value)
    set_attribute = cap.get(cam_cap_attribute)
    if set_attribute != value:
        raise ValueError(
            f"Given {control_option_label} level `{value}` nor {control_option_label} "
            f"control is not supported by the camera."
        )


def video_file_check(file_path: str) -> None:
    """
    Checks if file path given by <file_path> is a video file.

    Args:
        file_path (str): File path.

    Returns (None):

    Exceptions:
        IOError: Raised if given file is not a video file.
    """
    shared_param_val.type_check(file_path, str)

    media_info = MediaInfo.parse(file_path)

    video_tracks = media_info.video_tracks
    if len(video_tracks) == 0:
        raise IOError(f"File given path by `{file_path}` is not a video file. Has empty video track.")

    video_track = video_tracks[0]
    if video_track.stream_size == 0:
        raise IOError(f"File given path by `{file_path}` is not a video file. Has zero stream size.")
