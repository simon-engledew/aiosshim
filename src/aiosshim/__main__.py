import asyncio
import aiosshim
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


NAME_PATTERN: re.Pattern = re.compile("(?P<name>.*)")


async def script(actor: aiosshim.Actor):
    actor.writeline("hello!")

    actor.write("Please enter your name: ")

    # match their input against a regular expression which will store the name in a capturing group called name
    groups = (await actor.expect(NAME_PATTERN)).groupdict()

    # log on the server-side that the user has connected
    logger.info("{name} just connected".format(**groups))

    # send a message back to the SSH client greeting it by name
    actor.writeline("Hello {name}!".format(**groups))


async def main():
    async with await aiosshim.start_server(script, "", 8022) as server:
        print("listening on", [socket.getsockname() for socket in server.sockets])
        await server.serve_forever()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
