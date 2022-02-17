import asyncio

from data_server.data_queue import DataQueue
from data_server.data_server import DataServer
from fake_data import DataFeeder
from pathlib import Path

import argparse

parser = argparse.ArgumentParser(description='Telemetry dashboard server')
parser.add_argument('--port', '-p', type=int, default=5678,
                    help='which port to serve the webserver on')
parser.add_argument('--save_dir', '-s', type=str, default='saved_data/',
                    help='Where to save/look for saved csv files of data')


async def main():
    args = parser.parse_args()
    # Write to file every 5 seconds, keep data in memory for 15 minutes.
    data_queue = DataQueue(Path(args.save_dir), 5, 900)
    data_server = DataServer(data_queue=data_queue, frequency=10, port=args.port)
    data_provider = DataFeeder(data_queue.add_row)

    tasks = [
        data_server.start_server(),
        data_provider.read_forever()
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
