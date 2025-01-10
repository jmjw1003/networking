import socket
import sys


def process_arguments() -> (str, int):
    """Returns the commandline arguments for url, port (optional)"""
    if len(sys.argv) == 1:
        return "example.com", 80
    if len(sys.argv) == 2:
        return sys.argv[1], 80
    else:
        return sys.argv[1], sys.argv[2]


def get_request(address: str, port: int | str, encoding: str = "ISO-8859-1") -> str:
    s = socket.socket()
    s.connect((address, port))
    get_request = f"GET / HTTP/1.1\r\nHost: {address}:{port}\r\nConnection: close\r\n\r\n"
    b = get_request.encode(encoding)
    s.sendall(b)
    res = ""
    while True:
        d = s.recv(4096)
        if len(d) == 0:
            break
        res += d.decode(encoding)
    return res


def main():
    address, port = process_arguments()
    response = get_request(address, port)
    print(response)
    return 0


if __name__ == "__main__":
    main()