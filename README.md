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

MIT License
===========
Copyright (C) 2012 Oren Held

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
