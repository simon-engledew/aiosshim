import asyncio
import asyncssh
import typing
import typeguard
import io
import logging
import re


logger = logging.getLogger(__name__)


@typeguard.typechecked
class Actor:
    def __init__(self, process: asyncssh.SSHServerProcess):
        self.process = process

    def write(self, text: str):
        self.process.stdout.write(text)

    def writeline(self, line: str):
        self.process.stdout.write(line + "\r\n")

    async def expect(self, predicate: typing.Union[typing.Pattern[str], str]):
        while True:
            line = await self.process.stdin.readline()
            if hasattr(predicate, "match"):
                match = predicate.match(line)
                if match is not None:
                    return match
            else:
                if predicate == line:
                    return line
        return None


@typeguard.typechecked
def handle_client_with_script(script: typing.Callable[[Actor], None]):
    async def handle_client(process: asyncssh.SSHServerProcess):
        await script(Actor(process))
        process.exit(0)

    return handle_client


class PermissiveSSHServer(asyncssh.SSHServer):
    def connection_made(self, chan):
        pass

    def connection_lost(self, exc):
        if exc is not None:
            logger.warning(repr(exc))
        pass

    def begin_auth(self, username):
        return True

    def public_key_auth_supported(self):
        return True

    def validate_public_key(self, username, key):
        return True


@typeguard.typechecked
async def start_server(
    script: typing.Callable[[Actor], None],
    host: str,
    port: int = 0,
    *,
    server_host_keys: typing.Union[
        str, typing.List[typing.Union[str, typing.Tuple[bytes, bytes]]]
    ] = "ssh_host_key"
) -> asyncio.base_events.Server:
    """
    Start a server running an actor process
    """

    return await asyncssh.create_server(
        PermissiveSSHServer,
        host,
        port,
        server_host_keys=server_host_keys,
        process_factory=handle_client_with_script(script),
    )


__all__ = ["start_server"]

