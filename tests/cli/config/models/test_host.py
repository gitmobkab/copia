from ipaddress import IPv4Address, IPv6Address

import pytest
from pydantic import ValidationError

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

    def test_invalid_host(self):
        with pytest.raises(ValidationError):
            make_profile(host="-bad-host")

    def test_empty_host(self):
        with pytest.raises(ValidationError):
            make_profile(host="")

    def test_host_with_spaces(self):
        with pytest.raises(ValidationError):
            make_profile(host="bad host")

    def test_label_leading_hyphen(self):
        with pytest.raises(ValidationError):
            make_profile(host="-label.com")

    def test_label_trailing_hyphen(self):
        with pytest.raises(ValidationError):
            make_profile(host="label-.com")

    def test_label_too_long(self):
        with pytest.raises(ValidationError):
            make_profile(host="a" * 64)

    def test_host_too_long(self):
        label = "a" * 63
        host = ".".join([label] * 5)
        with pytest.raises(ValidationError):
            make_profile(host=host)
