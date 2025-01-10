import logging
import socket
import sys


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def process_arguments(system_arguments: sys.argv) -> int:
    """Returns the commandline arguments for port (optional)"""
    if len(system_arguments) == 1:
        return 28333
    return system_arguments[1]


class WebServer:
    def __init__(self, port: int, encoding: str = "ISO-8859-1") -> None:
        # Port initialization
        self.port = port
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))
        # Pre compute responses
        self.get_response = self._get_response(encoding)

    def _get_response(self, encoding):
        server_response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!\r\n"
        byte_response = server_response.encode(encoding)
        return byte_response

    def listen(self, encoding: str = "ISO-8859-1"):
        self.s.listen()
        while True:
            new_socket, new_addr = self.s.accept()
            logger.info(f"Connection from address: {new_addr}")
            msg = ""
            while True:
                d = new_socket.recv(4096)
                chunk = d.decode(encoding)
                if chunk[-4:] == "\r\n\r\n":
                    msg += chunk
                    break
                msg += chunk
            new_socket.sendall(self.get_response)
            new_socket.close()


def main():
    port = process_arguments(sys.argv)
    web_server = WebServer(port)
    web_server.listen()


if __name__ == "__main__":
    main()
