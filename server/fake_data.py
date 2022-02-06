import asyncio
import random
import pandas as pd
FREQUENCY = 10  # frequency to send new data in Hz


def get_random_data():
    return {'timestamp': pd.Timestamp.now(),
            'float data': random.random(),
            'int data': random.randint(0, 360),
            'bool data': random.random() > 0.5}


def read_frame():
    return get_random_data()


class DataFeeder:
    def __init__(self, data_callback):
        self.data_callback = data_callback

    async def read_forever(self):
        print('Starting fake data generator')
        if FREQUENCY > 100:
            while True:
                for i in range(10):
                    self.data_callback(read_frame())
                await asyncio.sleep(10.0 / FREQUENCY)
        else:
            while True:
                self.data_callback(read_frame())
                await asyncio.sleep(1.0 / FREQUENCY)


