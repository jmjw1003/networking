import pytest
from src.conversion import IPv4Conversion


@pytest.fixture
def converter():
    return IPv4Conversion()


def test_ip_numeric_conv(converter):
    assert converter.convert_readable_ip_to_numeric("198.165.0.1") == 3332702209
    assert converter.convert_readable_ip_to_numeric("198.165.0.1".split(".")) == 3332702209
    assert converter.convert_readable_ip_to_numeric([0xc6, 0x33, 0x64, 0x0a]) == 3325256714


def test_numeric_ip_conv(converter):
    assert converter.convert_numeric_ip_to_readable(3332702209) == "198.165.0.1"
    assert converter.convert_numeric_ip_to_readable(0xc633640a) == "198.51.100.10"