import unittest
import myip_cmd
from mock import patch

SAMPLE_OUTPUT1 = """3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000\n    link/ether 10:0b:a9:81:ac:64 brd ff:ff:ff:ff:ff:ff\n    inet 192.168.1.102/24 brd 192.168.1.255 scope global wlan0\n    inet6 fe80::120b:a9ff:fe81:ac64/64 scope link \n       valid_lft forever preferred_lft forever"""

SAMPLE_OUTPUT2 = """1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN qlen 1000
    link/ether 00:21:cc:b9:cb:d5 brd ff:ff:ff:ff:ff:ff
    inet 1.2.3.4/8 brd 1.255.255.255 scope global eth0
3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
    link/ether 10:0b:a9:81:ac:64 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global wlan0
    inet6 fe80::120b:a9ff:fe81:ac64/64 scope link
       valid_lft forever preferred_lft forever
4: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
    link/ether 6a:5f:ce:b7:85:a7 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0"""

SAMPLE_IP_HASH1 = {"wlan0": "192.168.1.102"}

SAMPLE_IP_HASH2 = {"wlan0": "192.168.1.100",
                "eth0": "1.2.3.4",
                "virbr0": "192.168.122.1",
                "lo": "127.0.0.1",
                }

SAMPLE_OUTPUT_NO_IP_ASSIGNED = """2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN qlen 1000
    link/ether 00:21:cc:b9:cb:d5 brd ff:ff:ff:ff:ff:ff"""

class IpaddrParserTests(unittest.TestCase):
    @patch("commands.getstatusoutput")
    def test_one_interface(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT1)
        self.assertEquals(SAMPLE_IP_HASH1, myip_cmd.parse_ip_addr_cmd(["wlan0"]))

    @patch("commands.getstatusoutput")
    def test_multiple_interfaces(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT2)
        self.assertEquals(SAMPLE_IP_HASH2, myip_cmd.parse_ip_addr_cmd([]))

    @patch("commands.getstatusoutput")
    def test_interface_with_no_ip_assigned(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT_NO_IP_ASSIGNED)
        self.assertEquals({}, myip_cmd.parse_ip_addr_cmd([]))
    

class myipTests(unittest.TestCase):
    @patch("commands.getstatusoutput")
    def test_get_primary_ip(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT2)
        config = myip_cmd.parse_args([])
        ips = myip_cmd.get_ips(config)
        self.assertEquals(["1.2.3.4"], ips)

    @patch("commands.getstatusoutput")
    def test_get_all_ips(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT2)
        config = myip_cmd.parse_args(["--all"])
        ips = myip_cmd.get_ips(config)
        self.assertEquals(["1.2.3.4", "192.168.1.100", "192.168.122.1"], ips)

    @patch("commands.getstatusoutput")
    def test_specific_interface(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT1)
        config = myip_cmd.parse_args(["wlan0"])
        ips = myip_cmd.get_ips(config)
        self.assertEquals(["192.168.1.102"], ips)

