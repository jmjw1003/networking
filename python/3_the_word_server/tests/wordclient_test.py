import pytest
import random
from src.wordclient import get_next_word_packet, extract_word

# Constants for the functions
WORD_LEN_SIZE = 2
BUFFER_SIZE = random.randint(1, 4096)  # Tested manually with 1, 5, 4096
MAX_WORD_SIZE = 256
LONG_STR = "a" * MAX_WORD_SIZE

# Global packet_buffer for the functions
packet_buffer = b''

@pytest.fixture
def mock_socket(mocker):
    # Mock the socket's recv method
    mocked_socket = mocker.MagicMock()    

    # Define side effects for s.recv (simulating data being received)
    mocked_socket.recv.side_effect = [
        b'\x00\x05hello',
        b'\x00\x04good',
        MAX_WORD_SIZE.to_bytes(WORD_LEN_SIZE, "big") + LONG_STR.encode(),
        b''
    ]

    return mocked_socket


def test_get_next_word_packet(mock_socket):
    global packet_buffer

    # Call the function with the mocked socket
    word1 = get_next_word_packet(mock_socket)
    word2 = get_next_word_packet(mock_socket)
    word3 = get_next_word_packet(mock_socket)
    word4 = get_next_word_packet(mock_socket)

    # Test that the first word packet is correct
    assert word1 == b'\x00\x05hello'
    # Test that the second word packet is correct
    assert word2 == b'\x00\x04good'
    # Test that the third word packet is correct
    assert word3 == MAX_WORD_SIZE.to_bytes(WORD_LEN_SIZE, "big") + LONG_STR.encode()
    # Test that the function returns None when the stream ends
    assert word4 is None


def test_extract_word():
    word1 = extract_word(b'\x00\x05hello')
    word2 = extract_word(b'\x00\x04good')
    word3 = extract_word(MAX_WORD_SIZE.to_bytes(WORD_LEN_SIZE, "big") + LONG_STR.encode())

    assert word1 == "hello"
    assert word2 == "good"
    assert word3 == LONG_STR
