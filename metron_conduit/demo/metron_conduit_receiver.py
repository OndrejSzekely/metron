"""
*Metron Conduit* demo receiver to test the component.
"""

import asyncio
import socket
import argparse
import typing
from vidgear.gears.asyncio import NetGear_Async
import cv2

DOCKER_HOST_OPTION: typing.Final[str] = "docker_host"
CONTAINER_OPTION: typing.Final[str] = "container"


async def receiver_func() -> None:
    """
    Connects to *Metron Conduit*, receives and processes frames. In case of <DOCKER_HOST_OPTION>, it shows received
    frames. In case of <CONTAINER_OPTION>, it only prints numpy arrays into console, because Docker containers do not
    have displaying option by default.

    Returns (None):
    """
    async for frame in client.recv_generator():
        print(frame)

        if args.host_type == DOCKER_HOST_OPTION:
            cv2.imshow("Output Frame", frame)
            _ = cv2.waitKey(1) & 0xFF

        await asyncio.sleep(0.00001)


def get_ip_address(host_type: str) -> typing.Optional[str]:
    """
    Returns IP address based on host type.

    Args:
        host_type (str): Host type.

    Returns (typing.Optional[str]): IP address string representation. If none of the conditions is matched,
        <None> is returned.
    """
    if host_type == DOCKER_HOST_OPTION:
        return "127.0.0.1"
    if host_type == CONTAINER_OPTION:
        return socket.gethostbyname(socket.gethostname())

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Metron Conduit - Demo", description="Consumes video stream provided by Metron Conduit."
    )
    parser.add_argument(
        "--host-type",
        "-t",
        choices=[DOCKER_HOST_OPTION, CONTAINER_OPTION],
        required=True,
        help="Defines where `Metron Conduit - Demo` is run.",
    )
    parser.add_argument(
        "--port", "-p", type=str, required=True, help="Defines port on which Metron Conduit is streaming."
    )
    args = parser.parse_args()

    ip_address = get_ip_address(args.host_type)

    client = NetGear_Async(receive_mode=True, address=ip_address, port=args.port).launch()

    asyncio.set_event_loop(client.loop)
    try:
        client.loop.run_until_complete(receiver_func())
    except (KeyboardInterrupt, SystemExit):
        pass

    if args.host_type == DOCKER_HOST_OPTION:
        cv2.destroyAllWindows()
    client.close()
