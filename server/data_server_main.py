import asyncio

from data_server.data_queue import DataQueue
from data_server.data_server import DataServer
from fake_data import DataFeeder


async def main():
    data_queue = DataQueue('', 123, 123)
    data_server = DataServer(data_queue=data_queue, frequency=5)
    data_provider = DataFeeder(data_queue.add_row)

    tasks = [
        data_server.start_server(),
        data_provider.read_forever()
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
