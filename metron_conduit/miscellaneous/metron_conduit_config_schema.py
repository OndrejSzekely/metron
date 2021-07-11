"""
The module provides *Structured Config Schema* to validate Hydra configs - config parameters and their type.
It does not validate parameter values.
"""


from dataclasses import dataclass
import typing
from hydra.core.config_store import ConfigStore


@dataclass
class SourceConnectorSchema:
    """
    Hydra Config Schema parent for all *Source Connectors*. Serves as *Abstract Connector* schema.
    """


@dataclass
class FileSourceSchema(SourceConnectorSchema):
    """
    Hydra Config Schema for *File Connector*.

    The class has all attributes from <source_connector.file_source.FileConnector> class, with the same meaning.

    Attributes:
        file_path (str): The same meaning as in FileConnector class. Has to be specified by user.
        transcoding_resolution (typing.List[int]): The same meaning as in FileConnector class.
            Has to be specified by user.
        _target_ (str): Path to *File Connector* class, which is used for automatic Hydra class instantiating.
    """

    file_path: str
    transcoding_resolution: typing.List[int]
    _target_: str = "metron_conduit.source_connector.file_source.FileConnector"


@dataclass
class UsbCamSourceSchema(SourceConnectorSchema):
    """
    Hydra Config Schema for *USB Camera Connector*.

    The class has all attributes from <source_connector.file_source.UsbCamConnector> class, with the same meaning.

    Attributes:
        camera_id (int): The same meaning as in UsbCamConnector class.
        cam_frame_res (typing.List[int]): The same meaning as in UsbCamConnector class.
            Has to be specified by user.
        cam_fps (int): The same meaning as in UsbCamConnector class.
        cam_brightness (typing.Optional[int]): The same meaning as in UsbCamConnector class.
        cam_contrast (typing.Optional[int]): The same meaning as in UsbCamConnector class.
        cam_saturation (typing.Optional[int]): The same meaning as in UsbCamConnector class.
        cam_hue (typing.Optional[int]): The same meaning as in UsbCamConnector class.
        cam_zoom (typing.Optional[int]): The same meaning as in UsbCamConnector class.
        cam_focus (typing.Optional[int]): The same meaning as in UsbCamConnector class.
        cam_autofocus (typing.Optional[int]): The same meaning as in UsbCamConnector class.
        cam_auto_wb (typing.Optional[int]): The same meaning as in UsbCamConnector class.
        _target_ (str): Path to *USB Camera Connector* class, which is used for automatic Hydra class instantiating.
    """

    # pylint: disable=too-many-instance-attributes
    # Addressing the same topic as exception in *USB Cam Connector* class.

    cam_fps: int
    camera_id: int
    cam_frame_res: typing.List[int]
    time_delay: int
    cam_brightness: typing.Optional[int] = None
    cam_contrast: typing.Optional[int] = None
    cam_saturation: typing.Optional[int] = None
    cam_hue: typing.Optional[int] = None
    cam_zoom: typing.Optional[int] = None
    cam_focus: typing.Optional[int] = None
    cam_autofocus: typing.Optional[int] = None
    cam_auto_wb: typing.Optional[int] = None
    _target_: str = "metron_conduit.source_connector.usb_cam_source.UsbCamConnector"


@dataclass
class StreamerWorkerSchema:
    """
    Hydra Config Schema for *Streamer Worker*.

    The class has all attributes from <video_streamer.streamer_worker.StreamerWorker> class, with the same meaning.

    Attributes:
        address (str): The same meaning as in StreamerWorker class.
        port (str): The same meaning as in StreamerWorker class.
        com_protocol (typing.Optional[str]): The same meaning as in StreamerWorker class.
        com_pattern (typing.Optional[int]): The same meaning as in StreamerWorker class.
        stream_frame_res (typing.List[int]): The same meaning as in StreamerWorker class.
        stream_fps (float): The same meaning as in StreamerWorker class.
        _target_ (str): Path to *Video Streamer* class, which is used for automatic Hydra class instantiating.
    """

    address: str
    port: str
    com_protocol: str
    com_pattern: int
    stream_frame_res: typing.List[int]
    stream_fps: float
    _target_: str = "metron_conduit.video_streamer.streamer_worker.StreamerWorker"


@dataclass
class VideoStreamerSchema:
    """
    Hydra Config Schema for *Video Streamer*.

    Defines configuration of *Streamer Worker* instances.

    Attributes:
        mshine_streamer_worker (StreamerWorkerSchema): *Streamer Worker* sending stream to *Metron Shine* component.
        mcore_streamer_worker (StreamerWorkerSchema): *Streamer Worker* sending stream to *Metron Core* component.
    """

    mshine_streamer_worker: StreamerWorkerSchema
    mcore_streamer_worker: StreamerWorkerSchema


@dataclass
class MetronConduitConfigSchema:
    """
    Main Hydra Config Schema for Metron Conduit.

    Attributes:
        source_connector (SourceConnectorSchema):  Particular *Source Connector*.
    """

    video_streamer: VideoStreamerSchema
    source_connector: SourceConnectorSchema


def metron_conduit_config_schema_registration(cf_instance: ConfigStore) -> None:
    """
    Registers Hydra Config Schema for *Metron Conduit*.

    Args:
        cf_instance (ConfigStore): ConfigStore instance.

    Returns (None):
    """
    cf_instance.store(name="metron_conduit_config_schema", node=MetronConduitConfigSchema)
    cf_instance.store(group="source_connector", name="file_source_schema", node=FileSourceSchema)
    cf_instance.store(group="source_connector", name="usb_cam_source_schema", node=UsbCamSourceSchema)
    cf_instance.store(group="video_streamer", name="base_streamer_worker_schema", node=StreamerWorkerSchema)
