from pathlib import Path

"""
Reference diagrams, each + represents a byte delimiter.
Note that TCP protocol is 6.

IP header:
+--------+--------+--------+--------+
|           Source Address          |
+--------+--------+--------+--------+
|         Destination Address       |
+--------+--------+--------+--------+
|  Zero  |  PTCL  |    TCP Length   |
+--------+--------+--------+--------+

TCP header:
0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""


class TCPFileUtils:
    def addr_to_bytes(self, addr: str) -> bytes:
        """Encodes an IPv4 string to bytes object"""
        nums = [int(i).to_bytes(1, "big") for i in addr.split(".")]
        return b''.join(nums)

    def read_tcp_addr_file(self, file: Path | str) -> list[bytes]:
        """Reads a TCP address file, encodes the addresses and returns [source, destination]"""
        file = Path(file)
        with open(file, "r") as f:
            tcp_addrs = f.read()[:-1]
        return [self.addr_to_bytes(i) for i in tcp_addrs.split(" ")]

    def read_tcp_data_file(self, file: Path | str) -> bytes:
        """Reads a binary TCP file and returns the data as a bytes object."""
        file = Path(file)
        with open(file, "rb") as f:
            tcp_data = f.read()
        return tcp_data


class TCPValidator:
    def __init__(self) -> None:
        # IP header constants
        self.TCP_PROTOCOL = b'0x06'
        self.ZERO = b'0x00'

    def build_psuedoheader(self, source: bytes, destination: bytes, tcp_data: bytes):
        """Builds an IP header for given source, destination and tcp data."""
        return source + destination + self.ZERO + self.TCP_PROTOCOL + len(tcp_data).to_bytes(length=2, byteorder="big")
    
    def get_tcp_checksum(self, tcp_data: bytes) -> int:
        """TCP Checksum is located in bytes 16 & 17."""
        return int.from_bytes(tcp_data[16:18], "big")

    def build_zero_checksum_tcp_data(self, tcp_data: bytes) -> bytes:
        """Takes TCP data and sets the checksum to zero so it can be used for validation calculations.
        
        If a segment contains an odd number of header and text octets to be checksummed, the last octet is padded on
        the right with zeros to form a 16 bit word for checksum purposes.
        """
        tcp_zero_cksum = tcp_data[:16] + b'\x00\x00' + tcp_data[18:]
        if len(tcp_zero_cksum) % 2 == 1:
            tcp_zero_cksum += b'\x00'
        return tcp_zero_cksum

    def calculate_tcp_checksum(self, validation_data: bytes) -> int:
        """Given a TCP payload with 0 checksum, calculates the checksum.
        
        The checksum field is the 16 bit one's complement of the
        one's complement sum of all 16 bit words in the header and text.
        """
        offset = 0  # Byte offset into data
        calculated_tcp_checksum = 0

        while offset < len(validation_data):
            # Slice 2 bytes out and get their value (word):
            word = int.from_bytes(validation_data[offset:offset+2], "big")
            calculated_tcp_checksum += word
            # Carry around
            calculated_tcp_checksum = (calculated_tcp_checksum & 0xffff) + (calculated_tcp_checksum >> 16)

            # Increment offset
            offset += 2

        # One's complement
        return (~calculated_tcp_checksum) & 0xffff

    def validate_tcp_checksum(self, source: bytes, destination: bytes, tcp_data: bytes) -> bool:
        # Build IP header
        pseudoheader = self.build_psuedoheader(source, destination, tcp_data)
        # Get TCP checksum from data
        tcp_checksum = self.get_tcp_checksum(tcp_data)
        # Build TCP data with checksum set to zero for validation
        zero_checksum_tcp_data = self.build_zero_checksum_tcp_data(tcp_data)
        # Combine IP header and TCP data for validation
        validation_data = pseudoheader + zero_checksum_tcp_data
        # Use combined data to calculate checksum
        calculated_checksum = self.calculate_tcp_checksum(validation_data)
        # Compare checksums
        return tcp_checksum == calculated_checksum


def main():
    tcp_utils = TCPFileUtils()
    tcp_validator = TCPValidator()
    
    for i in range(10):
        addr_file = f"./python/4_tcp_packet_validation/src/tcp_data/tcp_addrs_{i}.txt"
        tcp_file = f"./python/4_tcp_packet_validation/src/tcp_data/tcp_data_{i}.dat"
        source, destination = tcp_utils.read_tcp_addr_file(addr_file)
        tcp_data = tcp_utils.read_tcp_data_file(tcp_file)
        tcp_data_valid = tcp_validator.validate_tcp_checksum(source, destination, tcp_data)
        print("PASS") if tcp_data_valid else print("FAIL")
    

if __name__ == "__main__":
    main()

