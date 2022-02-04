from webserver import Webserver

import argparse

parser = argparse.ArgumentParser(description='Telemetry dashboard server')
parser.add_argument('--port', '-p', type=int, nargs=1, default=8080,
                    help='which port to serve the webserver on')
parser.add_argument('--debug', '-d', action='store_const', const=True, default=False,
                    help='run the webserver in debug mode')
parser.add_argument('--fakedata', '-f', action='store_const', const=True, default=False,
                    help='run with fake data')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.debug:
        print('Running webserver in debug mode!')
    webserver = Webserver(debug=args.debug, port=args.port)
    webserver.run()



