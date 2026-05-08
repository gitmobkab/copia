from ipaddress import IPv4Address, IPv6Address

from tests.cli.config.models.utils import make_profile


class TestHost:
    def test_valid_hostname(self):
        p = make_profile(host="localhost")
        assert str(p.host) == "localhost"

    def test_valid_domain(self):
        p = make_profile(host="db.myapp.com")
        assert str(p.host) == "db.myapp.com"

    def test_valid_ipv4(self):
        p = make_profile(host="192.168.1.1")
        host = p.host
        assert isinstance(host, IPv4Address)

    def test_valid_ipv6(self):
        p = make_profile(host="::1")
        assert isinstance(p.host, IPv6Address)