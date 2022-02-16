import asyncio
import json

import websockets
from websockets.exceptions import ConnectionClosed

from data_server.data_queue import DataQueue


class DataServer:
    def __init__(self, frequency, data_queue):
        self.data_queue = data_queue
        self.frequency = frequency
        self.clients = set()

    async def start_server(self):
        tasks = [
            websockets.serve(self.publisher, 'localhost', 5678),  # Start server & connect to new clients
            self.broadcast_forever(),  # Broadcast incomming data forever
            self.data_queue.stream_to_file()
        ]
        await asyncio.gather(*tasks)  # Run both tasks in parallel

    async def publisher(self, websocket):
        self.clients.add(websocket)
        try:
            await websocket.send(self.data_queue.read_all_data().to_json(orient='split'))  # Get new client "caught up" on all the old data
            await asyncio.Future()  # wait forever
        finally:
            self.clients.remove(websocket)  # This never happens unless there's an exception

    async def broadcast_data(self, data):
        json_data = data.to_json(orient='split')
        # print('Sending to ', len(self.clients), ' clients: ', json_data)
        for client in self.clients.copy():
            try:
                await client.send(json_data)
            except ConnectionClosed:
                # Close connection if a client disconnects
                self.clients.remove(client)

    async def broadcast_forever(self):
        while True:
            await asyncio.sleep(1.0 / self.frequency)
            await self.broadcast_data(self.data_queue.pop_new_data())
