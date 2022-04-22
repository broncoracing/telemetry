import asyncio

import settings
from data_server.data_queue import DataQueue
from data_server.data_server import DataServer
from pathlib import Path

import argparse


async def run_data_server(args, pipe=None):
    # Write to file every 5 seconds, keep data in memory for 15 minutes.
    data_queue = DataQueue(Path(args.save_dir), 5, 900)
    data_server = DataServer(data_queue=data_queue, frequency=10, port=args.ws_port)

    if args.fake_data:
        from data_reader.fake_data import DataFeeder
        data_provider = DataFeeder(data_queue.add_row)
    elif args.serial is not None:
        from data_reader.serial_can_data import DataFeeder
        print('Using serial for CAN data')
        data_provider = DataFeeder(data_queue.add_row, args.serial)
    else:
        from data_reader.can_data import DataFeeder
        data_provider = DataFeeder(data_queue.add_row)

    tasks = [
        data_server.start_server(),
        data_provider.read_forever()
    ]
    await asyncio.gather(*tasks)


def main(args, pipe=None):
    asyncio.run(run_data_server(args, pipe))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Telemetry data server')
    parser.add_argument('--ws_port', '-w', type=int, default=settings.WEBSOCKET_DEFAULT_PORT,
                        help='which port to serve the webserver on')
    parser.add_argument('--save_dir', '-s', type=str, default=settings.DATA_DIR,
                        help='Where to save/look for saved csv files of data')
    parser.add_argument('--fake_data', '-f', default=False, action='store_const', const=True,
                        help='Use fake generated data instead of reading from the CAN bus')
    parser.add_argument('--serial', default=None, type=str,
                        help='Use a serial device (Ex: /dev/ttyUSB0) instead of socketcan for input data')

    args = parser.parse_args()
    main(args)
