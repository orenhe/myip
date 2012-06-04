import commands
import logging
import sys
import argparse
import re
import platform

import parsing

# TODO detect primary interface by default route
# TODO check virtual interfaces (eth0:1) and funny iface names
# TODO check bonding/teaming
# TODO check IPless up interfaces

# Consts
BLACKLIST_IFACES_PREFIX = "lo"
INTERFACE_NAME_PREFIX_BY_PRIORITY = ["eth", "wlan", "en0", "en1"] # TODO move setting to OS-specific plugin
DEBUG_LEVEL = logging.WARNING # logging.DEBUG

logging.basicConfig(level=DEBUG_LEVEL)

# Globals
parse_ip_addr_cmd = None

def prioritize_ifaces(prio_list, keys):
    prioritized_list = []
    for prio in prio_list:
        cur_level = [k for k in keys if k.startswith(prio)]
        prioritized_list.extend(cur_level)

    # Add rest of the keys
    unprioritized_keys = [k for k in keys if k not in prioritized_list]

    prioritized_list.extend(unprioritized_keys)

    return prioritized_list

def parse_args(args):
    parse = argparse.ArgumentParser(description="myip: Simple tool to display the current IP")
    parse.add_argument('--all', const=True, action='store_const', dest="all_ips", help="show all IPs")
    parse.add_argument('interface', nargs='?', help="Show IP of a specific interface")
    config = parse.parse_args(args)

    return config

def generate_ip_list_ordered_by_iface(ip_hash, interface_list):
    ips = []
    for interface in interface_list:
        ips.append(ip_hash[interface])

    return ips

def get_ip_of_specific_interface(iface):
    return parse_ip_addr_cmd(iface)[iface]

def load_platform_support():
    # pylint: disable=W0603
    global parse_ip_addr_cmd
    os_name = platform.system().lower()

    if not parse_ip_addr_cmd:
        try:
            os_module = getattr(__import__("myip", fromlist=[os_name]), os_name)
            parse_ip_addr_cmd = os_module.parse_ip_addr_cmd
        except ImportError:
            logging.error("Failed loading platform %s support", os_name)

def get_ips(config):
    if config.interface: # interface param provided
        return [get_ip_of_specific_interface(config.interface)]

    ifaces_hash = parse_ip_addr_cmd()
    filtered_ifaces = [k for k in ifaces_hash.keys() if not k.startswith(BLACKLIST_IFACES_PREFIX)]

    ifaces_by_priority = prioritize_ifaces(INTERFACE_NAME_PREFIX_BY_PRIORITY, filtered_ifaces)
    if config.all_ips:
        # All interfaces
        ips = generate_ip_list_ordered_by_iface(ifaces_hash, ifaces_by_priority)
    else:
        # Primary interface only
        ips = generate_ip_list_ordered_by_iface(ifaces_hash, [ifaces_by_priority[0]])

    return ips
    
def main():
    load_platform_support()
    config = parse_args(sys.argv[1:])
    ips = get_ips(config)
    for ip in ips:
        print ip

if __name__ == "__main__":
    main()
