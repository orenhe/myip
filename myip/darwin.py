import re
import logging
import commands
from . import parsing

def parse_ip_addr_cmd(specific_iface=None):
    cmdline = "ifconfig"
    if specific_iface:
        cmdline += " {iface}".format(iface=specific_iface)
    stat, out = commands.getstatusoutput(cmdline)
    if stat != 0:
        raise Exception("Command '{cmdline}' failed (rc={rc}): {out}".format(cmdline=cmdline, rc=stat, out=out))

    iface_ip_hash = {}
    for block in parsing.split_output_into_blocks(out):
        logging.debug("Working on block '%s'", block)
        match = re.search("^([^:]+):", block)
        if not match:
            logging.error("Bad block, skipping: '%s'", block)
            continue

        iface = match.groups()[0]
        if not "UP" in block:
            logging.info("'%s' is not UP, skipping", iface)
            continue
        right_side = block.partition("inet ")[2]
        if right_side == "":
            logging.info("No IP found for iface %s", iface)
            continue
        ip = right_side.partition(" ")[0]
        iface_ip_hash[iface] = ip
    return iface_ip_hash


