import asyncio
import pytest
import aiosshim
import asyncssh
import re


TEST_KEY = [
    (
        b"""-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBxEyJ7K3hkNMYNCm5rmVApg1NmLdbKEFW7EQdES0oreQAAAJgvzwGLL88B
iwAAAAtzc2gtZWQyNTUxOQAAACBxEyJ7K3hkNMYNCm5rmVApg1NmLdbKEFW7EQdES0oreQ
AAAEAmjeNP84Xd2g+hB3m8cjCwzPe80+kH7JgkzK9Bbw5/hXETInsreGQ0xg0KbmuZUCmD
U2Yt1soQVbsRB0RLSit5AAAAEXNpbW9uQHVyaWVsLmxvY2FsAQIDBA==
-----END OPENSSH PRIVATE KEY-----
""",
        b"ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHETInsreGQ0xg0KbmuZUCmDU2Yt1soQVbsRB0RLSit5 aiosshim",
    )
]


@pytest.mark.asyncio
async def test_basic():
    async def echo(script: aiosshim.Actor):
        groups = (await script.expect(re.compile("(?P<value>.*)"))).groupdict()
        assert groups.get("value", None) == "test_echo"
        script.writeline("return {value}".format(**groups))

    async with await aiosshim.start_server(
        echo, "127.0.0.1", 0, server_host_keys=TEST_KEY
    ) as server:
        server: asyncio.base_events.Server

        _, port = next(socket.getsockname() for socket in server.sockets)
        async with asyncssh.connect("127.0.0.1", port, known_hosts=None) as client:
            client: asyncssh.SSHClientConnection
            async with client.create_process() as process:
                process: asyncssh.SSHClientProcess
                process.stdin.write("test_echo\n")
                assert await process.stdout.readline() == "return test_echo\r\n"

