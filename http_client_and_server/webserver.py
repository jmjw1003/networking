import logging
import socket
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def process_arguments() -> int:
    """Returns the commandline arguments for port (optional)"""
    if len(sys.argv) == 1:
        return 28333
    else:
        return sys.argv[1]


def main():
    server_response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!\r\n"
    byte_response = server_response.encode("ISO-8859-1")

    port = process_arguments()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    s.listen()
    while True:
        new_socket, new_addr = s.accept()
        logger.info(f"Connection from address: {new_addr}")  # Extension 1
        msg = ""
        while True:
            d = new_socket.recv(4096)
            chunk = d.decode("ISO-8859-1")
            if chunk[-4:] == "\r\n\r\n":
                msg += chunk
                break
            msg += chunk
        new_socket.sendall(byte_response)
        new_socket.close()


if __name__ == "__main__":
    main()