import re

IGNORED_DEFINES = [
    'CAN_BAUD',
]


def int_reader(data):
    output = 0
    for byte in data:
        output = output << 8
        output += byte
    return output


class Format:
    def __init__(self, offset, length, reader=int_reader, name=None):
        self.offset = offset
        self.length = length
        self.reader = reader
        self.name = name if name is not None else str(offset)

    def read(self, data):

        return self.reader(data[self.offset:self.offset + self.length])


data_formats = {
    'THERMOCOUPLE_1_ID': [Format(0, 2, name='Channel 1'), Format(2, 2, name='Channel 2'), Format(4, 2, name='Channel 3'), Format(6, 2, name='Channel 4')]
}


def define_to_readable_name(define_name):
    return ' '.join(word.title() for word in define_name.replace('_ID', '').split('_'))


def parse_can_ids(can_ids_path):
    # Open and read file
    with open(can_ids_path) as f:
        can_id_header = '\n'.join(f.readlines())

        # Remove comments
        pattern = re.compile(
            r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
            re.DOTALL | re.MULTILINE
        )
        can_id_header = re.sub(pattern, '', can_id_header)

        # Get only lines with #define
        lines = filter(lambda l: '#define' in l, can_id_header.split('\n'))

        # Shrink down excess whitespace
        lines = [re.sub(r'[\s]+', ' ', line) for line in lines]

        # split into parts by whitespace
        lines = [line.split(' ') for line in lines]

        # Regex to match CAN ID names
        name_pattern = re.compile(
            r'[A-Za-z][][A-Za-z_$0-9.]*',
            re.DOTALL | re.MULTILINE
        )

        # Iterate through line by line and add valid lines to the ID list
        defines = {}
        for line in lines:
            # ensure the format is #define (NAME) (CAN_ID)
            if len(line) >= 3 and re.match(name_pattern, line[1]) is not None:
                name = line[1]
                if name not in IGNORED_DEFINES:
                    defines[int(line[2], 0)] = (name, define_to_readable_name(name))

        return defines
