import pytest
from unittest.mock import patch, mock_open
from src.tcp_packet_validation import TCPFileUtils


@pytest.fixture
def tcp_utils():
    return TCPFileUtils()


def test_addr_to_bytes(tcp_utils):
    assert tcp_utils.addr_to_bytes("1.2.3.4") == b'\x01\x02\x03\x04'
    assert tcp_utils.addr_to_bytes("198.51.100.77") == b'\xc63dM'
    assert tcp_utils.addr_to_bytes("192.0.2.170") == b'\xc0\x00\x02\xaa'


def test_read_tcp_addr_file(tcp_utils):
    # The mock data to simulate file contents
    mock_data = "192.168.1.1 10.0.0.1\n"

    # Use patch to mock the open function within the context of read_tcp_addr_file
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = tcp_utils.read_tcp_addr_file("fake_file_path")
        
    # Assert that the result is the expected bytes encoding for the mock IPs
    assert result == [b'\xc0\xa8\x01\x01', b'\x0a\x00\x00\x01']
