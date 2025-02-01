from pathlib import Path

"""
IP pseudo header:
+--------+--------+--------+--------+
|           Source Address          |
+--------+--------+--------+--------+
|         Destination Address       |
+--------+--------+--------+--------+
|  Zero  |  PTCL  |    TCP Length   |
+--------+--------+--------+--------+
Each + represents a byte delimiter.
"""
# IP header constants
TCP_PROTOCOL = b'0x06' # TCP Procotol number is 6
ZERO = b'0x00'

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


# For local testing.
# import os
# os.chdir("./python/4_tcp_packet_validation/")


tcp_utils = TCPFileUtils()
source, destination = tcp_utils.read_tcp_addr_file("./src/tcp_data/tcp_addrs_0.txt")
print(source)
print(destination)
# source_bytes = tcp_utils.addr_to_bytes(source)
# destination_bytes = tcp_utils.addr_to_bytes(destination)

# tcp_data = tcp_utils.read_tcp_data_file("./src/tcp_data/tcp_data_0.dat")

# print(tcp_data)