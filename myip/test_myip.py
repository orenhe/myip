import unittest
import myip_cmd
import linux
import darwin
from mock import patch, Mock


SAMPLE_OUTPUT_LINUX = """1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN
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

SAMPLE_OUTPUT_LINUX_NO_IP_ASSIGNED = """2: eth0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc pfifo_fast state DOWN qlen 1000
    link/ether 00:21:cc:b9:cb:d5 brd ff:ff:ff:ff:ff:ff"""

SAMPLE_OUTPUT_DARWIN = """lo: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
        inet 127.0.0.1 netmask 0xff000000 
        inet6 ::1 prefixlen 128 
        inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1 
gif0: flags=8010<POINTOPOINT,MULTICAST> mtu 1280
stf0: flags=0<> mtu 1280
eth0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
        inet6 fe80::214:51ff:fe68:77e0%en0 prefixlen 64 scopeid 0x4 
        inet 1.2.3.4 netmask 0xffffff00 broadcast 192.168.1.255
        ether 00:14:51:68:77:e0 
        media: autoselect (10baseT/UTP <half-duplex>) status: active
        supported media: none autoselect 10baseT/UTP <half-duplex> 10baseT/UTP <half-duplex,hw-loopback> 10baseT/UTP <full-duplex> 10baseT/UTP <full-duplex,hw-loopback> 10baseT/UTP <full-duplex,flow-control> 100baseTX <half-duplex> 100baseTX <half-duplex,hw-loopback> 100baseTX <full-duplex> 100baseTX <full-duplex,hw-loopback> 100baseTX <full-duplex,flow-control> 1000baseT <full-duplex> 1000baseT <full-duplex,hw-loopback> 1000baseT <full-duplex,flow-control>
wlan0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
        inet6 fe80::214:51ff:fe68:77e0%en0 prefixlen 64 scopeid 0x4 
        inet 192.168.1.100 netmask 0xffffff00 broadcast 192.168.1.255
        ether 00:14:51:68:77:e0 
        media: autoselect (10baseT/UTP <half-duplex>) status: active
        supported media: none autoselect 10baseT/UTP <half-duplex> 10baseT/UTP <half-duplex,hw-loopback> 10baseT/UTP <full-duplex> 10baseT/UTP <full-duplex,hw-loopback> 10baseT/UTP <full-duplex,flow-control> 100baseTX <half-duplex> 100baseTX <half-duplex,hw-loopback> 100baseTX <full-duplex> 100baseTX <full-duplex,hw-loopback> 100baseTX <full-duplex,flow-control> 1000baseT <full-duplex> 1000baseT <full-duplex,hw-loopback> 1000baseT <full-duplex,flow-control>
en8: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
        ether 00:14:51:68:77:e1 
        media: autoselect (<unknown type>) status: inactive
        supported media: none autoselect 10baseT/UTP <half-duplex> 10baseT/UTP <half-duplex,hw-loopback> 10baseT/UTP <full-duplex> 10baseT/UTP <full-duplex,hw-loopback> 10baseT/UTP <full-duplex,flow-control> 100baseTX <half-duplex> 100baseTX <half-duplex,hw-loopback> 100baseTX <full-duplex> 100baseTX <full-duplex,hw-loopback> 100baseTX <full-duplex,flow-control> 1000baseT <full-duplex> 1000baseT <full-duplex,hw-loopback> 1000baseT <full-duplex,flow-control>
fw0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 4078
        lladdr 00:14:51:ff:fe:a8:a2:d2 
        media: autoselect <full-duplex> status: inactive
        supported media: autoselect <full-duplex>
virbr0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
        inet6 fe80::214:51ff:fe68:77e0%en0 prefixlen 64 scopeid 0x4 
        inet 192.168.122.1 netmask 0xffffff00 broadcast 192.168.1.255
        ether 00:14:51:68:77:e0 
        media: autoselect (10baseT/UTP <half-duplex>) status: active
        supported media: none autoselect 10baseT/UTP <half-duplex> 10baseT/UTP <half-duplex,hw-loopback> 10baseT/UTP <full-duplex> 10baseT/UTP <full-duplex,hw-loopback> 10baseT/UTP <full-duplex,flow-control> 100baseTX <half-duplex> 100baseTX <half-duplex,hw-loopback> 100baseTX <full-duplex> 100baseTX <full-duplex,hw-loopback> 100baseTX <full-duplex,flow-control> 1000baseT <full-duplex> 1000baseT <full-duplex,hw-loopback> 1000baseT <full-duplex,flow-control>"""

SAMPLE_IP_HASH2 = {"wlan0": "192.168.1.100",
                "eth0": "1.2.3.4",
                "virbr0": "192.168.122.1",
                "lo": "127.0.0.1",
                }



class IpaddrLinuxParsingTests(unittest.TestCase):

    @patch("commands.getstatusoutput")
    def test_one_interface(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT_LINUX)
        self.assertEquals(SAMPLE_IP_HASH2, linux.parse_ip_addr_cmd(["wlan0"]))

    @patch("commands.getstatusoutput")
    def test_multiple_interfaces(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT_LINUX)
        self.assertEquals(SAMPLE_IP_HASH2, linux.parse_ip_addr_cmd([]))

    @patch("commands.getstatusoutput")
    def test_interface_with_no_ip_assigned(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT_LINUX_NO_IP_ASSIGNED)
        self.assertEquals({}, linux.parse_ip_addr_cmd([]))
    
class ifconfigDarwinParsingTests(unittest.TestCase):
    @patch("commands.getstatusoutput")
    def test_one_interface(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT_DARWIN)
        self.assertEquals(SAMPLE_IP_HASH2, darwin.parse_ip_addr_cmd(["wlan0"]))
 
    @patch("commands.getstatusoutput")
    def test_multiple_interfaces(self, mock_getoutput):
        mock_getoutput.return_value = (0, SAMPLE_OUTPUT_DARWIN)
        self.assertEquals(SAMPLE_IP_HASH2, darwin.parse_ip_addr_cmd(["wlan0"]))
    

class myipHighLevelTests(unittest.TestCase):
    def tearDown(self):
        reload(myip_cmd)

    def test_get_primary_ip(self):
        generate_ip_hash = Mock()
        generate_ip_hash.return_value = SAMPLE_IP_HASH2
        myip_cmd.parse_ip_addr_cmd = generate_ip_hash
        
        config = myip_cmd.parse_args([])
        ips = myip_cmd.get_ips(config)
        self.assertEquals(["1.2.3.4"], ips)

    def test_get_all_ips(self):
        generate_ip_hash = Mock()
        generate_ip_hash.return_value = SAMPLE_IP_HASH2
        myip_cmd.parse_ip_addr_cmd = generate_ip_hash
 
        config = myip_cmd.parse_args(["--all"])
        ips = myip_cmd.get_ips(config)
        self.assertEquals(["1.2.3.4", "192.168.1.100", "192.168.122.1"], ips)

    def test_specific_interface(self):
        generate_ip_hash = Mock()
        generate_ip_hash.return_value = SAMPLE_IP_HASH2
        myip_cmd.parse_ip_addr_cmd = generate_ip_hash
 
        config = myip_cmd.parse_args(["wlan0"])
        ips = myip_cmd.get_ips(config)
        self.assertEquals(["192.168.1.100"], ips)

