import pandas as pd


class DataQueue:
    def __init__(self, csv_path, write_frequency, max_age):
        self.csv_path = csv_path
        self.write_frequency = write_frequency
        self.max_age = max_age
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
