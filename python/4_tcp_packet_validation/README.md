# Project: Validating a TCP packet

### Inputs
A sequence of pairs of files (./src/tcp_data/*):

- One contains the source and destination IPv4 addresses in dots-and-numbers notation.
- The other contains the raw TCP packet, both the TCP header and the payload.

### Outputs
- For each pair of files, print `PASS` if the TCP checksum is correct. Otherwise print `FAIL`.

### Banned functions
Usage of the `sockets` library is forbidden.

