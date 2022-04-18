def int_reader(data):
    output = 0
    for byte in data:
        output = output << 8
        output += byte
    return output


def bool_reader(data):
    return not all([b == 0 for b in data])


def scaled_reader(multiplier, offset=0):
    def reader(data):
        output = 0
        for byte in reversed(data):
            output = output << 8
            output += byte
        return float(output) * multiplier + offset

    return reader


class Format:
    def __init__(self, offset, length, reader=int_reader, name=None):
        self.offset = offset
        self.length = length
        self.reader = reader
        self.name = name if name is not None else str(offset)

    def read(self, data):

        return self.reader(data[self.offset:self.offset + self.length])