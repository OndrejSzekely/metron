"""
The script runs *Metron Conduit* component.
"""


import os
import hydra
from miscellaneous.metron_conduit_config_schema import metron_conduit_config_schema_registration
from miscellaneous import metron_conduit_utils
from shared import metron_globals
from shared.config import set_hydra_config
from shared.config_schema import create_structured_config_schema
from metron_conduit.video_streamer.streamer_manager import StreamerManager
from metron_conduit.miscellaneous.metron_conduit_config_schema import MetronConduitConfigSchema


@create_structured_config_schema(metron_conduit_config_schema_registration)
@hydra.main(
    config_path=f"{os.path.join(os.getcwd(), 'conf')}", config_name="metron_conduit_config"
)  # type: ignore[misc]
@set_hydra_config
def main(hydra_config: MetronConduitConfigSchema) -> None:  # pylint: disable=unused-argument
    """
    Main function of *Metron Conduit* component.

    Args:
        hydra_config (MetronConduitConfigSchema): Metron Conduit configuration parameters provided by Hydra's config.

    Returns (None):
    """
    source_connector = metron_conduit_utils.instantiate_source_connector()
    streamer_manager = StreamerManager(source_connector)
    metron_conduit_utils.setup_streamer_workers(streamer_manager, source_connector)

    with streamer_manager as video_streamer:
        metron_globals.event_loop.run_until_complete(video_streamer.gather_tasks())


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
