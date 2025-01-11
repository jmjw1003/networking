import logging
import os
import socket
import sys
from enum import Enum
from pathlib import Path


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
        
        # Server files
        self.server_files = os.listdir(Path("./files/"))  # Note this will not work if running the server from the root directory.

        # Pre-computed responses
        self.not_implemented = self._not_implemented_response()
        self.not_found = self._not_found_response()
        self.get = self._get_response()

    def _read_file(self, file_name: str) -> str:
        with open(f"./files/{file_name}", "r") as f:
            data = f.read()
        return data

    def _encode_msg(self, msg: str) -> bytes:
        return msg.encode(self.encoding)

    def _get_response(self, file_name: str | None = None) -> bytes:
        if not file_name:
            dir_options = f"Available files: {", ".join(self.server_files)}"
            server_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(dir_options)}\r\nConnection: close\r\n\r\n{dir_options}\r\n"
        else:
            content_type = file_name.split(".")[-1]
            content = self._read_file(file_name)
            server_response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\nConnection: close\r\n\r\n{content}\r\n"
        return self._encode_msg(server_response)
    
    def _not_implemented_response(self) -> bytes:
        server_response = "HTTP/1.1 501 Not Implemented\r\n"
        return self._encode_msg(server_response)
    
    def _not_found_response(self) -> bytes:
        server_response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found\r\n"
        return self._encode_msg(server_response)
    
    def _parse_request(self, request: str) -> bytes:
        request_lines = request.split("\r\n")
        request_type, full_path, _ = request_lines[0].split(" ")
        logger.info(f"{request_type} {full_path}")
        if request_type != RequestTypes.GET.name:
            return self.not_implemented
        file_name = os.path.split(full_path)[-1]
        if full_path == "/" or file_name == "/":
            return self.get
        if file_name not in self.server_files:
            return self.not_found
        return self._get_response(file_name)
        
    def listen(self) -> None:
        """
        Sets the server to listen for incoming connections, fetches a new socket from the OS,
        receives message stream and then sends a response before closing the connection
        """
        self.s.listen()
        logger.info(f"WebServer running, listening on port: {self.port}.")
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
            response_msg = self._parse_request(msg)
            
            new_socket.sendall(response_msg)
            new_socket.close()


def main():
    port = process_arguments(sys.argv)
    web_server = WebServer(port)
    web_server.listen()


if __name__ == "__main__":
    main()
