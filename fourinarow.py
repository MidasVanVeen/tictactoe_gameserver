from websockets import serve
import asyncio

gamearray = []

async def handle_join(name, roomcode):
    while True:
        for game in gamearray:
            if game[0]
    pass

async def handle_move(name, roomcode):
    pass

async def handle_get(websocket, roomcode):
    pass

async def handle_connection(websocket):
    while True:
        try:
            args = await websocket.recv()
            args = args.split(",")
            command = args[0]
            if command == "join":
                await handle_join(args[1],args[2])
            elif command == "move":
                await handle_move(args[1], args[2])
            elif command == "get":
                await handle_get(websocket, args[1])
        except:
            pass

async def main():
    with serve(handle_connection, "0.0.0.0", 8888):
        await asyncio.Future()

asyncio.run(main())
