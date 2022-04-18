import asyncio
from pathlib import Path
from collections import defaultdict

from data_reader.can_ids_parser import parse_can_ids, data_formats
import serial
import struct
from dataclasses import dataclass
import threading

FREQUENCY = 20  # Hz

CAN_FRAME_FORMAT = "< 2s ? L B 8s B"
CAN_FRAME_SIZE = struct.calcsize(CAN_FRAME_FORMAT)


@dataclass
class CanFrame:
    arbitration_id: int
    data: bytearray


def read_can_message(bts):
    if len(bts) != CAN_FRAME_SIZE:
        raise ValueError('Invalid input size, expected {} bytes but got {}'.format(CAN_FRAME_SIZE, len(bts)))

    try:
        if not verify_can_checksum(bts):
            raise ValueError('Invalid checksum')


        can_message = struct.unpack(CAN_FRAME_FORMAT, bts)

        # print(f'checksum works, {can_message}')

        if can_message[0] != b'\x5A\xA5':  # Check sync word
            raise ValueError('No sync word found')

        # print('Found sync bytes')

        arb_id = can_message[2]
        dlc = can_message[3]
        if dlc > 8 :
            raise ValueError('DLC too large!')
        data = can_message[4][:dlc]
        return CanFrame(arbitration_id=arb_id, data=data)
    except ValueError:
        return None
    except struct.error:
        return None


def write_can_message(can_frame: CanFrame):
    dlc = len(can_frame.data)
    if dlc > 8:
        raise ValueError('Only 8 bytes of data can be packed into a CAN frame')

    buf = bytearray(struct.pack(CAN_FRAME_FORMAT, b'\xA5\x5A', False, can_frame.arbitration_id, dlc, can_frame.data, 0))
    buf[-1] = calc_can_checksum(buf)
    return buf


def calc_can_checksum(bts):
    checksum = sum(b for b in bts[:16]) # Don't include last byte
    return checksum % 256


def verify_can_checksum(bts):
    return calc_can_checksum(bts) == bts[16]


class DataFeeder:
    def __init__(self, data_callback, serial_port='/dev/ttyUSB0'):
        self.data_callback = data_callback
        can_ids_path = Path(__file__).parent.parent / 'can-ids' / 'CAN_IDS.h'
        self.can_ids = parse_can_ids(can_ids_path)
        self.latest_data = defaultdict(None)
        # self.latest_data['placeholder'] = 1
        # print(can_ids)
        try:
            self.bus = serial.Serial(serial_port, baudrate=230400)
            # # TODO Start read_forever in a loop
            self.listener_thread = threading.Thread(target=self.listen_forever, daemon=True)
            self.listener_thread.start()
        except OSError as e:
            print(e)
            print('Failed to connect to serial port. No data will be available.')

    def listen_forever(self):
        buf = bytearray()
        print('running')
        while True:
            # print('f')
            new_byte = self.bus.read(1)
            buf += new_byte
            if len(buf) >= CAN_FRAME_SIZE:
                # print('trying to decode')
                # print(buf)
                buf = buf[-CAN_FRAME_SIZE:]
                maybe_frame = read_can_message(buf)
                if maybe_frame is not None:
                    # print('frame received!')
                    # print(maybe_frame)
                    self.message_received(maybe_frame)
                    buf = bytearray()

    def message_received(self, message):
        # print(message)
        if message.arbitration_id in self.can_ids:
            name = self.can_ids[message.arbitration_id]
        else:
            name = (str(message.arbitration_id), 'ID#{}'.format(message.arbitration_id))

        if name[0] in data_formats:
            formats = data_formats[name[0]]
            for fmt in formats:
                self.latest_data[name[1] + ' ' + fmt.name] = fmt.read(message.data)
                # print(name[1] + ' ' + format.name, format.read(message.data))
        else:
            for i in range(len(message.data)):
                self.latest_data[name[1] + ' ' + str(i)] = message.data[i]
        # print(name)

    async def read_forever(self):
        while True:
            if len(self.latest_data) != 0:
                self.data_callback(self.latest_data)
            # self.latest_data.clear()
            await asyncio.sleep(1.0 / FREQUENCY)
