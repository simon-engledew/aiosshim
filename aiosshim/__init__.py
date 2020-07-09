import asyncio
import asyncssh
import typing
import typeguard


async def handle_client(process: asyncssh.SSHServerProcess):
    process.stdout.write('connected!')
    process.exit(0)


class PermissiveSSHServer(asyncssh.SSHServer):
    def connection_made(self, chan):
        pass

    def connection_lost(self, exc):
        pass

    def begin_auth(self, username):
        return True

    def public_key_auth_supported(self):
        return True

    def validate_public_key(self, username, key):
        return True


@typeguard.typechecked
async def start_server(host: str, port: int) -> asyncio.base_events.Server:
    return await asyncssh.create_server(
        PermissiveSSHServer,
        host,
        port,
        server_host_keys=[
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
        ],
        process_factory=handle_client,
    )

__all__ = ['start_server']
