import asyncio
import datetime
from pathlib import Path
import os
import pandas as pd


class DataQueue:
    FUTURE = pd.Timestamp("2100-01-01")  # TODO: Update this in 87 years so that the telemetry dashboard doesn't break

    def __init__(self, csv_dir: Path, write_delay, max_age):
        self.write_delay = write_delay
        self.max_age = max_age
        # Initialize this in the past so that we don't miss any data
        self.last_written_timestamp = pd.Timestamp("1970-01-01")
        timestamp = datetime.datetime.now().isoformat(sep='_', timespec='seconds')
        self.csv_file_path = csv_dir / (timestamp + '.csv')
        print('Saving data to: {}'.format(self.csv_file_path))

        self.data = pd.DataFrame(columns=('timestamp',))
        self.data = self.data.set_index('timestamp')
        self.new_data = pd.DataFrame(columns=('timestamp',))
        self.new_data = self.new_data.set_index('timestamp')

    def add_row(self, data):
        if 'timestamp' in data.keys():
            now = data['timestamp']
            data.pop('timestamp')
        else:
            now = pd.Timestamp.now()
        try:
            self.new_data.loc[now] = data
        except ValueError:
            # columns don't line up, fix it
            for key in data.keys():
                if key not in self.new_data.columns:
                    self.new_data[key] = 0
            self.new_data.loc[now] = data

        # print(self.data)
        # print(self.data.to_json(orient='columns'))

    def pop_new_data(self):
        d = self.new_data
        self.data = self.data.append(d)
        self.new_data = pd.DataFrame(columns=('timestamp',))
        self.new_data = self.new_data.set_index('timestamp')
        return d

    def read_all_data(self):
        return self.data

    # Save the unwritten data to a csv file.
    # Note: This will mess up the CSV format if the columns change between writes, because the header won't be updated
    def save_to_file(self):
        # Get the new data
        df = self.data.loc[self.last_written_timestamp:self.FUTURE]
        # Update the last written timestamp
        if len(self.data) > 0:
            self.last_written_timestamp: pd.Timestamp = self.data.index[-1]
        # Write to CSV in append mode, and only write a header if the file doesn't exist
        # (so it's at the top of the file).
        df.to_csv(self.csv_file_path, mode='a', header=not os.path.exists(self.csv_file_path))

        # Truncate the saved data to prevent it from filling memory over time.
        # This is done *after* writing so that there's no chance data is lost.
        self.data = self.data.loc[self.last_written_timestamp - pd.Timedelta(self.max_age):self.FUTURE]

    async def stream_to_file(self):
        while True:
            await asyncio.sleep(self.write_delay)
            self.save_to_file()
