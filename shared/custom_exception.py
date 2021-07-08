"""
This file defines custom exceptions.
"""


import typing
from shared import param_validators as shared_param_val


class IOCamDevError(IOError):
    """
    Camera device is not found exception.

    Attributes:
        message (str): Exception message.
    """

    def __init__(self, msg: typing.Union[str, None] = None, accessed_cam_id: typing.Union[int, None] = None):
        """
        Two ways of use.

        Pass <accessed_cam_id> argument, then error template message is used, but msg should not be passed in.
        See the sample code snippet. If bot are passed, <msg> and <accessed_cam_id>, then <accessed_cam_id> is
        favoured and template message is used. This means that the same output is obtained with the following three
        calls:
        ```
        IOCamDevError(accessed_cam_id=0)
        IOCamDevError("some error msg", accessed_cam_id=0)
        IOCamDevError(msg="some error msg", accessed_cam_id=0)
        ```

        If <accessed_cam_id> is not passed then no error template message is used and the message argument is used.

        If no input argument is passed, than empty error message is used.

        Args:
            msg (typing.Union[str, None]): String to be used as an error message, it is optional.
            accessed_cam_id (typing.Union[int]): Accessed camera id for which exception is raised, it is optional.
        """
        shared_param_val.type_check(accessed_cam_id, (int, type(None)))
        shared_param_val.type_check(msg, (str, type(None)))
        msg = msg or ""
        msg = repr(msg)  # convert anything to string

        if accessed_cam_id is not None:
            self.message = f"Camera device `{accessed_cam_id}` is not found."
        else:
            self.message = msg

        super().__init__(self.message)

    def __str__(self) -> str:
        """
        Used to get string representation of the error.

        Returns (str): String error representation.

        """
        return self.message
