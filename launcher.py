import argparse
import textwrap

import ifaddr

from tc import DegradeInvoker
from tc.generic import Generic, GenericCommand
from configparser import ConfigParser
import os

#todo: statistiche, NAT, gestione con un iterable della lista dei profili,
# inserimento guidato dei profili e cancellazione, LQL library


def check_interface(interface):
    iface_list = ifaddr.get_adapters()
    for adapter in iface_list:
        if interface == adapter.nice_name:
            return interface
    else:
        raise argparse.ArgumentTypeError("Interface " + interface + " NOT found")


if __name__ == '__main__':
    config = ConfigParser()
    config.read(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')))
    parser = argparse.ArgumentParser(prog='traffic_conditioner',
    formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''\
         Usage of this application
         --------------------------------
             sudo python3 -i <interface> 
             
         The explicit rate limit is to be done...  
         '''))
    parser.add_argument(
        '-i', '--interface',
        default='eth0',
        type=check_interface,
        help='Specify interface for conditioning. \ndefault: %(default)s. \nAll attributes can be found in config.ini',
    )
    parser.add_argument(
        '-p', '--profile',
        default='Gentle',
        required= True,
        help='Specify profile for conditioning. \ndefault: %(default)s. \nAll attributes can be found in config.ini',
    )

    args = parser.parse_args()
    print(args.interface)

    invoker = DegradeInvoker(
            GenericCommand(
                Generic(config, args.interface, args.profile)
            ))
    invoker.invoke()
