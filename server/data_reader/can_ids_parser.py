import re

from data_reader.can_formats import scaled_reader, Format, bool_reader

IGNORED_DEFINES = [
    'CAN_BAUD',
]

data_formats = {
    'BCM_STATUS_ID': [  # TODO Add format once implemented in BCM firmware

    ],

    'STEERING_WHEEL_ID': [
        Format(0, 1, name='DRS State',  reader=bool_reader),
        Format(1, 1, name='Upshift',    reader=bool_reader),
        Format(2, 1, name='Downshift',  reader=bool_reader),
    ],

    'THERMOCOUPLE1_ID': [
        Format(0, 2, name='Channel 1'),
        Format(2, 2, name='Channel 2'),
        Format(4, 2, name='Channel 3'),
        Format(6, 2, name='Channel 4')
    ],
    'THERMOCOUPLE2_ID': [
        Format(0, 2, name='Channel 1'),
        Format(2, 2, name='Channel 2'),
        Format(4, 2, name='Channel 3'),
        Format(6, 2, name='Channel 4')
    ],

    'ECU1_ID': [
        Format(0, 2, name="Engine RPM", reader=scaled_reader(ms_first=True)),
        Format(2, 2, name="Lambda", reader=scaled_reader(multiplier=1.0/1000.0, ms_first=True)),
    ],
    'ECU2_ID': [
        Format(0, 1, name="Oil Temperature",        reader=scaled_reader(1.0)),
        Format(1, 2, name="ECT",                    reader=scaled_reader(1.0 / 10.0)),
        Format(3, 2, name="Intake Air Temperature", reader=scaled_reader(1.0 / 10.0)),
        Format(5, 2, name="Rad Temp",               reader=scaled_reader(1.0 / 10.0)),
    ],
    'ECU3_ID': [
        Format(0, 2, name="Oil Pressure",    reader=scaled_reader(1.0)),         # TODO Set scaling correctly
        Format(4, 2, name="Battery Voltage", reader=scaled_reader(1.0 / 1000.0)),
    ],

    'DBW_SENSORS_ID': [
        Format(0, 1, name="APPS",       reader=scaled_reader(10.0)),           # TODO Set scaling correctly
        Format(1, 1, name="APPS (sub)", reader=scaled_reader(10.0)),           # TODO Set scaling correctly
        Format(2, 1, name="TPS",        reader=scaled_reader(10.0)),           # TODO Set scaling correctly
        Format(3, 1, name="TPS (sub)",  reader=scaled_reader(10.0)),           # TODO Set scaling correctly
    ],

    'BRAKE_PRESSURE_ID': [
        Format(0, 2, name="BSE", reader=scaled_reader(ms_first=True)),
    ],
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
