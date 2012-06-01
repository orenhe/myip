import os
import commands
import logging
import sys
import argparse
import re

# TODO detect primary interface by default route
# TODO check virtual interfaces (eth0:1) and funny iface names
# TODO check bonding/teaming
# TODO check IPless up interfaces

# Consts
IP_BIN = "/sbin/ip"
BLACKLIST_IFACES = "lo"
INTERFACE_NAME_PREFIX_BY_PRIORITY = ["eth", "wlan"]
DEBUG_LEVEL = logging.WARNING # logging.DEBUG

logging.basicConfig(level=DEBUG_LEVEL)

def split_output_into_blocks(out):
    cur_entry = ""
    first_line = True
    for line in out.split("\n"):
        if first_line:
            first_line = False
            cur_entry += line + "\n"
            continue

        if not line.startswith(" "):
            yield cur_entry
            cur_entry = line + "\n"
        else:
            cur_entry += line + "\n"

    yield cur_entry # last but not least
        
def parse_ip_addr_cmd(specific_iface=None):
    cmdline = "{ip_bin} addr show".format(ip_bin=IP_BIN)
    if specific_iface:
        cmdline += " dev {iface}".format(iface=specific_iface)
    stat, out = commands.getstatusoutput(cmdline)
    if stat != 0:
        raise Exception("Command '{cmdline}' failed (rc={rc}): {out}".format(cmdline=cmdline, rc=stat, out=out))

    iface_ip_hash = {}
    for block in split_output_into_blocks(out):
        logging.debug("Working on block '%s'", block)
        match = re.search("^\d+:\s+([^:]+):", block)
        if not match:
            logging.error("Bad block, skipping: '%s'", block)
            continue

        iface = match.groups()[0]
        if not "UP" in block:
            logging.info("'%s' is not UP, skipping", iface)
            continue
        right_side = block.partition(" inet ")[2]
        if right_side == "":
            logging.info("No IP found for iface %s", iface)
            return None
        ip = right_side.partition("/")[0]
        iface_ip_hash[iface] = ip
    return iface_ip_hash

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


def get_ips(config):
    if config.interface: # interface param provided
        return [get_ip_of_specific_interface(config.interface)]

    ifaces_hash = parse_ip_addr_cmd()
    filtered_ifaces = [k for k in ifaces_hash.keys() if k not in BLACKLIST_IFACES]

    ifaces_by_priority = prioritize_ifaces(INTERFACE_NAME_PREFIX_BY_PRIORITY, filtered_ifaces)
    if config.all_ips:
        # All interfaces
        ips = generate_ip_list_ordered_by_iface(ifaces_hash, ifaces_by_priority)
    else:
        # Primary interface only
        ips = generate_ip_list_ordered_by_iface(ifaces_hash, [ifaces_by_priority[0]])

    return ips
    
def main():
    config = parse_args(sys.argv[1:])
    ips = get_ips(config)
    for ip in ips:
        print ip

if __name__ == "__main__":
    main()
