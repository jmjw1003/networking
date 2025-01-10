import logging
import socket
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def process_arguments(system_arguments: sys.argv) -> dict[str: str | int]:
    """Returns the commandline arguments for address, port (optional), payload (optional)"""
    match len(system_arguments):
        case 1:
            return {"address": "example.com", "port": 80}
        case 2:
            return {"address": system_arguments[1], "port": 80}
        case 3:
            return {"address": system_arguments[1], "port": int(system_arguments[2])}

    return {"address": system_arguments[1], "port": int(system_arguments[2]), "payload": system_arguments[3]}


class WebClient:
    def web_request(self, arguments: dict[str: str | int]) -> str:
        """In reality the user should choose the request type but in this case it's just being fixed based on cli args"""
        if arguments.get("payload"):
            return self._post_request(**arguments)
        else:
            return self._get_request(**arguments)

    def _get_request(self, address: str, port: int, encoding: str = "ISO-8859-1") -> str:
        """Makes a get request to an address, encoding set to web default."""
        s = socket.socket()
        s.connect((address, port))
        get_request = f"GET / HTTP/1.1\r\nHost: {address}:{port}\r\nConnection: close\r\n\r\n"
        b = get_request.encode(encoding)
        s.sendall(b)
        res =  ""
        while True:
            d = s.recv(4096)
            if len(d) == 0:
                break
            res += d.decode(encoding)
        return res
    
    def _post_request(self, address: str, port: int, payload: str, encoding: str = "ISO-8859-1") -> str:
        """Makes a post request with a simple text payload, encoding set to web default"""
        s = socket.socket()
        s.connect((address, port))
        post_request = f"""POST / HTTP1.1\r\n
        Host: {address}:{port}\r\n
        Content-Type: text/html\r\n
        Content-Length: {len(payload)}\r\n
        \r\n
        {payload}\r\n
        \r\n"""
        b = post_request.encode(encoding)
        s.sendall(b)
        res =  ""
        while True:
            d = s.recv(4096)
            if len(d) == 0:
                break
            res += d.decode(encoding)
        return res


def main():
    arguments = process_arguments(sys.argv)
    web_client = WebClient()
    client_response = web_client.web_request(arguments)
    logger.info(client_response)


if __name__ == "__main__":
    main()