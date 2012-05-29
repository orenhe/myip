import os
import commands
import logging

IP_BIN = "/sbin/ip"
BLACKLIST_IFACES = "lo"
IFACES_BY_PRIORITY = ["eth", "wlan"]
DEBUG_LEVEL = logging.WARNING # logging.DEBUG

logging.basicConfig(level=DEBUG_LEVEL)

def get_list_of_ifaces():
    sysfs_net_location = "/sys/class/net"
    ifaces = os.listdir(sysfs_net_location)

    return ifaces

def get_iface_ip_hash(ifaces):
    iface_ip_hash = {}
    for iface in ifaces:
        cmdline = "{ip_bin} addr show dev {iface}".format(ip_bin=IP_BIN, iface=iface)
        stat, out = commands.getstatusoutput(cmdline)
        if stat != 0:
            raise Exception("Command '{cmdline}' failed (rc={rc}): {out}".format(cmdline=cmdline, rc=stat, out=out))
        right_side = out.partition(" inet ")[2]
        if right_side == "":
            logging.info("No IP found for iface %s", iface)
            continue
        ip = right_side.partition("/")[0]
        iface_ip_hash[iface] = ip

    return iface_ip_hash

def prioritize_keys(prio_list, keys):
    prioritized_list = []
    for prio in prio_list:
        cur_level = [k for k in keys if k.startswith(prio)]
        prioritized_list.extend(cur_level)

    return prioritized_list


def main():
    ifaces = get_list_of_ifaces()
    ifaces_hash = get_iface_ip_hash(ifaces)
    filtered_keys = [k for k in ifaces_hash if k not in BLACKLIST_IFACES]
    prioritized_keys = prioritize_keys(IFACES_BY_PRIORITY, filtered_keys)
    # print the first one
    print ifaces_hash[prioritized_keys[0]]
    
