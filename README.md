myip - a simple tool for displaying the current IP
==================================================
After 30 years of TCP/IP, it's about time to have a tool that simply displays an IP.
The current popular tools (ifconfig, ip addr show) provide complex output and argument set, while usually we run
them in order to simply get an answer to the question "which IP(s) are configured on this host?".

myip is intended to be used by both scripts and humans.

API may be added later.

Installing
==========
1. `git clone git://github.com/orenhe/myip.git`
2. `sudo pip install myip/` 
 * Replace `myip/` with path to myip sources
 * Uninstall using `pip uninstall myip`

Usage
=====
`myip` - prints the primary IP.

`myip --all` - prints all IPs configured on the system

`myip <iface name>` - prints the IP of given interface, e.g. _eth0_.

License
=======
Licensed under the MIT license.
