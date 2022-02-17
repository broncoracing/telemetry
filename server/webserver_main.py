from webserver import Webserver
import argparse

parser = argparse.ArgumentParser(description='Telemetry dashboard server')
parser.add_argument('--port', '-p', type=int, default=8080,
                    help='which port to serve the webserver on')
parser.add_argument('--debug', '-d', action='store_const', const=True, default=False,
                    help='run the webserver in debug mode')
parser.add_argument('--save_dir', '-s', type=str, default='saved_layouts/',
                    help='Where to save/look for saved layouts')


def main():
    args = parser.parse_args()
    if args.debug:
        print('Running webserver in debug mode!')

    webserver = Webserver(debug=args.debug, port=args.port, save_dir=args.save_dir)
    webserver.run()


if __name__ == '__main__':
    main()



