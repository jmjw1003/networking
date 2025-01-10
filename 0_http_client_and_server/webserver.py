import logging
import socket
import sys
from enum import Enum


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class RequestTypes(Enum):
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    CONNECT = "CONNECT"


def process_arguments(system_arguments: sys.argv) -> int:
    """Returns the commandline arguments for port (optional)"""
    if len(system_arguments) == 1:
        return 28333
    return system_arguments[1]


class WebServer:
    def __init__(self, port: int, encoding: str = "ISO-8859-1") -> None:
        self.encoding = encoding
        # Port initialization
        self.port = port
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))
        # Pre computed responses
        self.get_response = self._get_response()
        self.head_response = self._head_response()
        self.not_implemented = self._not_implemented()
        # Logging goes brrr
        logger.info(f"WebServer running, listening on port: {self.port}.")

    def _encode_msg(self, msg: str) -> bytes:
        return msg.encode(self.encoding)

    def _get_response(self) -> bytes:
        """For some reason using @cached_property decorator didn't work with this function, so just pre computing in __init__"""
        server_response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!\r\n"
        return self._encode_msg(server_response)
    
    def _head_response(self) -> bytes:
        server_response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\n"
        return self._encode_msg(server_response)

    def _not_implemented(self) -> bytes:
        server_response = "HTTP/1.1 501 Not Implemented\r\n"
        return self._encode_msg(server_response)
    
    def _post_response(self, payload: str) -> bytes:
        server_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(payload)}\r\nConnection: close\r\n\r\{payload}\r\n"
        return self._encode_msg(server_response)
    
    def _status_and_response(self, msg_type: str, payload: str | None = None) -> (int, bytes):
        if msg_type == RequestTypes.GET.name:
            return 200, self.get_response
        if msg_type == RequestTypes.POST.name:
            return 200, self._post_response(payload)
        if msg_type not in RequestTypes:
            return 400, "Bad request: unknown request type"
        return 501, self.not_implemented
        
    def listen(self) -> None:
        """
        Sets the server to listen for incoming connections, fetches a new socket from the OS,
        receives message stream and then sends a response before closing the connection
        """
        self.s.listen()
        while True:
            new_socket, new_addr = self.s.accept()
            logger.info(f"Connection from address: {new_addr}")
            msg = ""
            while True:
                d = new_socket.recv(4096)
                chunk = d.decode(self.encoding)
                if chunk[-4:] == "\r\n\r\n":
                    msg += chunk
                    break
                msg += chunk
            msg_type = msg.split(" ")[0]
            logger.info(msg_type)
            status, response_msg = self._status_and_response(msg_type, msg)
            new_socket.sendall(response_msg)
            new_socket.close()


def main():
    port = process_arguments(sys.argv)
    web_server = WebServer(port)
    web_server.listen()


if __name__ == "__main__":
    main()
