import asyncio
import aiosshim


async def main():
    async with await aiosshim.start_server("", 8022) as server:
        print("listening on", [socket.getsockname() for socket in server.sockets])
        await server.serve_forever()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
