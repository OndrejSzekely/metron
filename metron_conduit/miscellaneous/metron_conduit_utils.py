"""
This file contains small domain-free functions specific to *Metron Conduit*.
"""

import hydra
from metron_conduit.miscellaneous.metron_conduit_config_schema import MetronConduitConfigSchema
from metron_conduit.video_streamer.streamer_manager import StreamerManager
from metron_conduit.video_streamer.streamer_worker import StreamerWorker
from metron_conduit.source_connector.abstract_source import AbstractConnector
from shared.config import GetHydraConfig


@GetHydraConfig
def instantiate_source_connector(hydra_config: MetronConduitConfigSchema) -> AbstractConnector:
    """
    Instantiates particular *Source Connector* based on configuration provided by Hydra framework.

    Args:
        hydra_config (MetronConduitConfigSchema): Metron Conduit configuration parameters provided by Hydra's config.

    Returns (AbstractConnector): Instantiated *Source Connector*.
    """
    return hydra.utils.instantiate(hydra_config.source_connector)


@GetHydraConfig
def setup_streamer_workers(
    hydra_config: MetronConduitConfigSchema, streamer_manager: StreamerManager, source_connector: AbstractConnector
) -> None:
    """
    Creates two *Streamer Worker* instances based on Hydra's configuration. One instance is used to stream video to
    *Metron Core*, the second instance streams video to *Metron Shine*. Instances are registered to *Streamer Manager*.

    Args:
        hydra_config (MetronConduitConfigSchema): Metron Conduit configuration parameters provided by Hydra's config.
        streamer_manager (StreamerManager): *Streamer Manager* which operates registered *Streamer Workers*.
        source_connector (AbstractConnector): *Source Connector* instance which is used for async frames generator.

    Returns (None):
    """
    # mypy [attr-defined] is ignored because <hydra_config> is a duck type object
    for streamer_worker_name in hydra_config.video_streamer:  # type: ignore[attr-defined]
        instantiated_streamer_worker: StreamerWorker = hydra.utils.instantiate(
            # mypy [index] is ignored because <hydra_config> is a duck type object
            hydra_config.video_streamer[streamer_worker_name]  # type: ignore[index]
        )
        instantiated_streamer_worker.set_frame_generator(source_connector)
        streamer_manager.register_streamer_worker(instantiated_streamer_worker)
