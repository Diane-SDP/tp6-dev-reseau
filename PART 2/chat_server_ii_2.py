import asyncio

async def handle_client_msg(reader, writer):
    while True:

        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')

        if data == b'':
            break

        message = data.decode()
        print(f"Received {message!r} from {addr!r}")

        writer.write(f"Hello {addr}".encode())
        await writer.drain()

async def main():

    server = await asyncio.start_server(handle_client_msg, '127.0.0.1', 13337)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
