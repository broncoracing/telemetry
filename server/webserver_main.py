import settings
from webserver import Webserver
import argparse


def main(args, pipe=None):
    if args.debug:
        print('Running webserver in debug mode!')

    webserver = Webserver(debug=args.debug, port=args.port, save_dir=args.layout_dir)
    webserver.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Telemetry dashboard server')
    parser.add_argument('--port', '-p', type=int, default=settings.WEBSERVER_DEFAULT_PORT,
                        help='which port to serve the webserver on')
    parser.add_argument('--debug', '-d', action='store_const', const=True, default=False,
                        help='run the webserver in debug mode')
    parser.add_argument('--layout_dir', '-l', type=str, default=settings.LAYOUT_DIR,
                        help='Where to save/look for saved layouts')

    args = parser.parse_args()
    main(args)
