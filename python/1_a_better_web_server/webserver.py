import logging
import mimetypes
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


class ContentService:
    """Web server was getting a bit too fat so moving all of the content generation to here"""
    def __init__(self, port: int, encoding: str = "ISO-8859-1") -> None:
        self.encoding = encoding
        self.resources_dir = "./resources/"
        self.server_files = os.listdir(f"{self.resources_dir}/files/")
        self.server_files_html = "".join([f'<li><a href="localhost:{port}/{i}">{i}</a></li>' for i in self.server_files])

    def _read_file(self, file_name: str | Path, read_type: str = "rb") -> bytes:
        with open(file_name, read_type) as f:
            data = f.read()
        return data

    def _encode_msg(self, msg: str) -> bytes:
        return msg.encode(self.encoding)
    
    def get_response(self, file_name: str | None = None) -> bytes:
        if not file_name:
            file_name = "home.html"
            homepage = self._read_file(Path(f"{self.resources_dir}/{file_name}"), read_type="r")
            homepage = homepage.replace("[SERVER_FILES]", self.server_files_html)
            content = self._encode_msg(homepage)
        else:
            content = self._read_file(Path(f"{self.resources_dir}/files/{file_name}"))
        
        content_type = mimetypes.guess_type(file_name)[0]
        response_partial = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}; charset={self.encoding.lower()}\r\nContent-Length: {len(content)}\r\nConnection: close\r\n\r\n"
        response = self._encode_msg(response_partial) + content + b"\r\n"
        return response

    def not_implemented_response(self) -> bytes:
        server_response = "HTTP/1.1 501 Not Implemented\r\n"
        return self._encode_msg(server_response)
    
    def not_found_response(self) -> bytes:
        server_response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found\r\n"
        return self._encode_msg(server_response)


class WebServer:
    def __init__(self, port: int, content_service: ContentService, encoding: str = "ISO-8859-1") -> None:
        self.encoding = encoding
        self.content_service = content_service

        # Port initialization
        self.port = port
        self.s = socket.socket()
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('', port))
        
        # Pre-computed responses, should probably do it for all files but I'm lazy..
        self.not_implemented = self.content_service.not_implemented_response()
        self.not_found = self.content_service.not_found_response()
        self.get = self.content_service.get_response()

    def _parse_request(self, request: str) -> bytes:
        request_lines = request.split("\r\n")
        request_type, full_path, _ = request_lines[0].split(" ")
        logger.info(f"{request_type} {full_path}")
        if request_type != RequestTypes.GET.name:
            return self.not_implemented
        file_name = os.path.split(full_path)[-1]
        if full_path == "/" or file_name == "/":
            return self.get
        if file_name not in self.content_service.server_files:
            return self.not_found
        return self.content_service.get_response(file_name)
        
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
                if chunk.endswith("\r\n\r\n"):
                    msg += chunk
                    break
                msg += chunk
            response_msg = self._parse_request(msg)
            
            new_socket.sendall(response_msg)
            new_socket.close()


def main():
    port = process_arguments(sys.argv)
    content_service = ContentService(port)
    web_server = WebServer(port, content_service)
    web_server.listen()


if __name__ == "__main__":
    main()
