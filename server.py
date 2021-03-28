import asyncio
import websockets
import time
import json
import threading

connected = set()
outreg = [{"player": "1", "data": []}, {"player": "2", "data": []}]

async def socket_broadcast(data):
    for client in connected:
           await client.send(str(data))

async def hello(websocket, path):
    global outreg
    i = 0
    connected.add(websocket)
    try:
        while i == 0:
            try:
                await socket_broadcast(json.dumps(outreg))
                x = await websocket.recv()
                try:
                    datareg = json.loads(x)
                    if datareg['player'] == 1:
                        outreg[0]["data"] = datareg["data"]
                    elif datareg['player'] == 2:
                        outreg[1]["data"] = datareg["data"]
                    #print(json.dumps(datareg)+"\n\n\n"+json.dumps(outreg))
                    await socket_broadcast(json.dumps(outreg))
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
                connected.remove(websocket)
                i = 1
    finally:
        # Unregister.
        connected.remove(websocket)
    
        
start_server = websockets.serve(hello, "localhost", 8765)

loop = asyncio.get_event_loop()

def loop_in_thread():
    loop.run_until_complete(start_server)
    loop.run_forever()

t = threading.Thread(target=loop_in_thread, args=tuple())
t.start()


print("hello")
