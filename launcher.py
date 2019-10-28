import argparse
import textwrap

import ifaddr

from tc.gentle import Gentle
from configparser import ConfigParser
import os


def check_interface(interface):
    iface_list = ifaddr.get_adapters()
    for adapter in iface_list:
        if interface == adapter.nice_name:
            return interface
    else:
        raise argparse.ArgumentTypeError("Interface " + interface + " NOT found")


if __name__ == '__main__':
    config = ConfigParser()
    config.read(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../config.ini')))
    parser = argparse.ArgumentParser(prog='traffic_conditioner',
    formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
         Usage of this application
         --------------------------------
             traffic_conditioner -i <interface> -r <rate limit>
             
         The rate limit is to be done...  
         '''))
    parser.add_argument(
        '-i', '--interface',
        default='eth0',
        type=check_interface,
        help='Specify interface for conditioning. \ndefault: %(default)s. \nAll attributes can be found in config.ini',
    )

    args = parser.parse_args()
    print(args.accumulate(args.interface))

    obj = Gentle(config, args.interface)
    obj.make_command()
