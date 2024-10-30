import asyncio

global CLIENTS
CLIENTS = {}

global LASTROOM
LASTROOM = 0

async def handle_client_msg(reader, writer):
    global LASTROOM 
    addr = writer.get_extra_info('peername')
    firstmsg = False
    if addr not in CLIENTS :
        firstmsg = True
    while True:

        data = await reader.read(1024)

        if data == b'':
            CLIENTS.pop(addr)
            for client, infos in CLIENTS.items() :
                if client != addr :
                    infos["w"].write(f"Annonce : {pseudo} a quitté la chatroom".encode())
                    await infos["w"].drain()
            break

        message = data.decode()
        print(f"Message received from {addr[0]}:{addr[1]} : {message}")
        if firstmsg :
            if message[:6] != "Hello|" or len(str(message).split('|')) != 3 :
                print("le premier msg n'est pas au bon format (Hello|<PSEUDO>|<ROOM>)")
                CLIENTS.pop(addr)
                break
            room = str(message).split('|')[2]
            if room == "n" :
                numroom = "room" + str(LASTROOM + 1)
                LASTROOM = LASTROOM + 1
            elif int(room) <= LASTROOM :
                numroom = "room" + room
            else : 
                print(f"room invalide : {room}")
                break
            pseudo = str(message).split('|')[1]
            if numroom not in CLIENTS:
                CLIENTS[numroom] = {}
            CLIENTS[numroom][addr] = {"r" : reader, "w" : writer, "pseudo" : pseudo}
            firstmsg = False
            for client, infos in CLIENTS[numroom].items() :
                infos["w"].write(f"Annonce : {pseudo} a rejoint la chatroom {numroom}".encode())
                await infos["w"].drain()
        else :
            pseudo = CLIENTS[numroom][addr]["pseudo"]
            for client, infos in CLIENTS[numroom].items() :
                if client != addr :
                    infos["w"].write(f"{pseudo} a dit : {message}".encode())
                    await infos["w"].drain()

async def main():

    server = await asyncio.start_server(handle_client_msg, '127.0.0.1', 13337)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
