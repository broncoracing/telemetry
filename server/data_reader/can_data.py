import asyncio
from pathlib import Path
from collections import defaultdict

from data_reader.can_ids_parser import parse_can_ids, data_formats
import can

FREQUENCY = 20  # Hz


class DataFeeder:
    def __init__(self, data_callback):
        self.data_callback = data_callback
        can_ids_path = Path(__file__).parent.parent / 'can-ids' / 'CAN_IDS.h'
        self.can_ids = parse_can_ids(can_ids_path)
        self.latest_data = defaultdict(None)
        self.latest_data['placeholder'] = 1
        # print(can_ids)
        try:
            self.bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=250000)
            self.notifier = can.Notifier(self.bus, [self.message_received], loop=asyncio.get_running_loop())
        except OSError as e:
            print(e)
            print('Failed to connect to CAN bus. No data will be available.')

    def message_received(self, message):
        # print(message)
        if message.arbitration_id in self.can_ids:
            name = self.can_ids[message.arbitration_id]
        else:
            name = str(message.arbitration_id)

        if name[0] in data_formats:
            formats = data_formats[name[0]]
            for format in formats:
                self.latest_data[name[1] + ' ' + format.name] = format.read(message.data)
                # print(name[1] + ' ' +  format.name, format.read(message.data))
        else:
            for i in range(len(message.data)):
                self.latest_data[name[1] + ' ' + str(i)] = message.data[i]
        # print(name)


    async def read_forever(self):
        while True:
            self.data_callback(self.latest_data)
            # self.latest_data.clear()
            await asyncio.sleep(1.0 / FREQUENCY)
