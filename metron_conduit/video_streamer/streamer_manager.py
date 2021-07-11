"""
*Video Streamer* sends out video stream, obtained by particular *Source Connector*, to other Metron components.

This file contains *Streamer Manager* class which orchestrates *Streamer Worker* class instances.
"""

from __future__ import annotations  # allowing future references -> return class under which return value is returned
import typing
import asyncio
from metron_conduit.video_streamer.streamer_worker import StreamerWorker
from metron_conduit.source_connector.abstract_source import AbstractConnector
from shared import param_validators as shared_param_val


class StreamerManager:
    """
    *Streamer Manager* acts like orchestrator of *Streamer Worker* instances, which are registered to it. This allows
    to broadcast the same stream with various configurations. The class communicates with *Source Connector* and
    passes frame by frame to registered *Streamer Worker* instances.

    Attributes:
        _streamer_workers (typing.List[streamer_worker.StreamerWorker]): Registered *Stream Worker* instances which
            broadcast stream provided by *Source Connector` instance <StreamerManager._source_connector>.
        _source_connector (abstract_source.AbstractConnector): A particular source connector inherited from
            `Abstract Connector`. All registered `Streamer Worker` instances in <StreamerManager._streamer_workers>
            broadcast this stream.
    """

    def __init__(self, source_connector: AbstractConnector):
        """
        Stores all attributes needed to orchestrate stream broadcasting.

        Args:
            source_connector (abstract_source.AbstractConnector): A particular source connector inherited from
                `Abstract Connector`. All registered `Streamer Worker` instances in <StreamerManager._streamer_workers>
                broadcast this stream.
        """
        shared_param_val.type_check(source_connector, AbstractConnector)

        self._streamer_workers: typing.List[StreamerWorker] = []
        self._source_connector = source_connector

    def register_streamer_worker(self, stream_worker: StreamerWorker) -> None:
        """
        Registers `Streamer Worker` instance to be used for broadcasting of stream provided by `Source Connector`
        instance <StreamerManager._source_connector>.

        Args:
            stream_worker (streamer_worker.StreamerWorker): `Streamer Worker` instance which will be registered. It will
                broadcast stream given by `Source Connector` instance <StreamerManager._source_connector>.

        Returns (None):
        """
        shared_param_val.type_check(stream_worker, StreamerWorker)

        self._streamer_workers.append(stream_worker)

    def __enter__(self) -> StreamerManager:
        """
        Context manager __entry__ method.

        Returns (StreamerManager): Itself. Prepares all registered `Streamer Worker` instances for broadcasting.
        """
        self._source_connector.__enter__()

        for streamer_worker in self._streamer_workers:
            streamer_worker.__enter__()

        return self

    def __exit__(
        self,
        exc_type: typing.Optional[Exception],
        exc_val: typing.Optional[typing.Any],
        exc_tb: typing.Any,
    ) -> None:
        """
        Context manager __exit__ method. Stops broadcasting of all registered `Streamer Worker` instances.

        Args:
            exc_type (typing.Optional[Exception]): Exception type.
            exc_val (typing.Optional[typing.Any]): Exception value.
            exc_tb (typing.Any): Exception traceback.

        Returns (None):
        """

        for streamer_worker in self._streamer_workers:
            streamer_worker.__exit__(exc_type, exc_val, exc_tb)

        self._source_connector.__exit__(exc_type, exc_val, exc_tb)

    def gather_tasks(self) -> asyncio.Future:
        """
        Gathers tasks of all registered *Streamer Worker* instances and creates asyncio.Future.

        Returns (asyncio.Future): Gathered *Streamer Worker* instance tasks.
        """
        tasks = []
        for streamer_worker in self._streamer_workers:
            tasks.append(streamer_worker.get_streaming_task())

        return asyncio.gather(*tasks)
