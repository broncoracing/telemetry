import subprocess as sp
import sys
import argparse
import webserver_main
import data_server_main
import atexit
import time
import settings

TERMINATE_TIMEOUT = 3


# Returns a function that will be called at exit to end the data server process.
def cleanup(process):
    def cleanup_func():
        process.terminate()
        wait_time = 0
        while process.poll() is None:
            if wait_time >= TERMINATE_TIMEOUT:
                process.kill()
                return
            time.sleep(0.1)

    return cleanup_func


def main(args):
    # Split args based on which program they correspond to
    data_server_args = ["--ws_port", str(args.ws_port),
                        '--save_dir', str(args.save_dir),
                        '--serial', str(args.serial)]
    if args.fake_data:
        data_server_args.append('--fake_data')

    web_server_args = ["--port", str(args.port),
                       '--layout_dir', str(args.layout_dir)]
    if args.debug:
        web_server_args.append('--debug')

    # Start the data server and web server and add an exit callback to terminate them when this program ends
    data_server_proc = sp.Popen([sys.executable, data_server_main.__file__, *data_server_args])
    atexit.register(cleanup(data_server_proc))

    web_server_proc = sp.Popen([sys.executable, webserver_main.__file__, *web_server_args])
    atexit.register(cleanup(web_server_proc))

    # Wait forever, or until both things crash
    data_server_proc.wait()
    web_server_proc.wait()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Telemetry dashboard server')
    # Dashboard server args
    parser.add_argument('--port', '-p', type=int, default=settings.WEBSERVER_DEFAULT_PORT,
                        help='which port to serve the webserver on')
    parser.add_argument('--debug', '-d', action='store_const', const=True, default=False,
                        help='run the webserver in debug mode')
    parser.add_argument('--layout_dir', '-l', type=str, default=settings.LAYOUT_DIR,
                        help='Where to save/look for saved layouts')

    # Data server args
    parser.add_argument('--ws_port', '-w', type=int, default=settings.WEBSOCKET_DEFAULT_PORT,
                        help='which port to serve the webserver on')
    parser.add_argument('--save_dir', '-s', type=str, default=settings.DATA_DIR,
                        help='Where to save/look for saved csv files of data')
    parser.add_argument('--fake_data', '-f', default=False, action='store_const', const=True,
                        help='Use fake generated data instead of reading from the CAN bus')
    parser.add_argument('--serial', default=None, type=str,
                        help='Use a serial device (Ex: /dev/ttyUSB0) instead of socketcan for input data')

    args = parser.parse_args()
    main(args)
