# Author: Midas
# back-end code voor de online boter kaas en eieren game

from websockets import serve
import asyncio
import json
import time

gamearray = []

async def emptystate():
     return [[0 for c in range(3)] for r in range(3)]

async def handle_join(args):
    roomcode = args[1]
    playername = args[2]
    while True:
        done = False
        for game in gamearray:
            if game[0] == roomcode:
                if len(game[1]) < 2 and playername not in game[1]:
                    game[1].append(playername)
                done = True
        if done: break
        gamearray.append([roomcode,[playername],await emptystate(),0,[False,"",[0,0,0]]])

async def check_win(grid):
    r = 0
    c = 0
    d = 0
    for row in grid:
        if row[0] == row[1] == row[2] != 0:
            r = grid.index(row) + 1
    for i in range(3):
        if grid[0][i] == grid[1][i] == grid[2][i] != 0:
            c = i + 1
    if grid[0][0] == grid[1][1] == grid[2][2] != 0:
        d = 1
    if grid[2][0] == grid[1][1] == grid[0][2] != 0:
        d = 2
    return [r,c,d]

async def check_draw(grid):
    for row in grid:
        for i in row:
            if i == 0:
                return False
    return True

async def handle_move(args):
    roomcode = args[1]
    playername = args[2]
    x = int(args[3])
    y = int(args[4])
    for game in gamearray:
        if game[0] == roomcode:
            if playername in game[1] and len(game[1]) == 2:
                if game[3] == game[1].index(playername):
                    if game[2][y][x] == 0:
                        if game[1].index(playername) == 0:
                            char = 'X'
                            game[3] = 1
                        elif game[1].index(playername) == 1:
                            char = 'O'
                            game[3] = 0
                        game[2][y][x] = char
                        win = await check_win(game[2])
                        if win != [0,0,0]:
                            game[4][0] = True
                            game[4][1] = playername
                            game[4][2] = win
                        draw = await check_draw(game[2])
                        if draw:
                            game[4][0] = True
                            game[4][1] = "Niemand"
            print(game)

async def clear_game(game):
    await asyncio.sleep(2)
    gamearray.remove(game)

async def handle_get(websocket, args):
    roomcode = args[1]
    array = []
    for game in gamearray:
        if game[0] == roomcode:
            array.append(game[1][game[3]])
            array.append(game[2])
            array.append(game[4])
            jsonstr = json.dumps(array)
            try:
                await websocket.send(jsonstr)
            except:
                pass
            if game[4][0]:
                await clear_game(game)

async def handle_connection(websocket):
    while True:
        try:
            message = await websocket.recv()
        except:
            pass
        args = message.split(",")
        if args[0] == "join":
            await handle_join(args)
        elif args[0] == "move":
            await handle_move(args)
        elif args[0] == "get":
            await handle_get(websocket, args)

async def main():
    async with serve(handle_connection, "0.0.0.0", 4444):
        await asyncio.Future()
    
if __name__ == "__main__":
    asyncio.run(main())
