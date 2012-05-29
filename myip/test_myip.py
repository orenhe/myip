import unittest
import myip
from mock import patch

SAMPLE_OUTPUT1 = """3: wlan0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000\n    link/ether 10:0b:a9:81:ac:64 brd ff:ff:ff:ff:ff:ff\n    inet 192.168.1.102/24 brd 192.168.1.255 scope global wlan0\n    inet6 fe80::120b:a9ff:fe81:ac64/64 scope link \n       valid_lft forever preferred_lft forever"""

SAMPLE_EXPECTED_HASH1 = {"wlan0": "192.168.1.102"}

class MyIpTests(unittest.TestCase):
    @patch("commands.getoutput")
    def test_get_ip_hash(self, mock_getoutput):
        mock_getoutput.return_value = SAMPLE_OUTPUT1
        self.assertEquals(SAMPLE_EXPECTED_HASH1, myip.get_iface_ip_hash(["wlan0"]))
