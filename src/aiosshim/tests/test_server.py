import asyncio
import pytest
import aiosshim
import asyncssh


@pytest.mark.asyncio
async def test_server():
    async with await aiosshim.start_server("127.0.0.1", 0) as server:
        server: asyncio.base_events.Server

        _, port = next(socket.getsockname() for socket in server.sockets)
        async with asyncssh.connect("127.0.0.1", port, known_hosts=None) as client:
            client: asyncssh.SSHClientConnection
            async with client.create_process() as process:
                process: asyncssh.SSHClientProcess
                assert await process.stdout.readline() == "connected!"
