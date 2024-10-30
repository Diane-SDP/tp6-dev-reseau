import asyncio
import socket
import sys
import time
import aioconsole

async def async_input(writer) :
    print("Tape ton pseudo :")
    firstmsg = True
    while True :
        msg = await aioconsole.ainput()
        if firstmsg :
            writer.write(f"Hello|{msg}".encode())
            firstmsg = False
        else :
            writer.write(msg.encode())
        await writer.drain()

async def async_receive(reader) :
    while True :
        # lire des données qui arrive du serveur
        data = await reader.read(1024)
        if data == b'':
            print("Serveur déconnecté")
            sys.exit()
        print(data.decode())


async def main():
    reader, writer = await asyncio.open_connection(host="127.0.0.1", port=13337)
    tasks = [ async_input(writer), async_receive(reader) ]
    await asyncio.gather(*tasks)


    

if __name__ == "__main__": 
    asyncio.run(main())


sys.exit()