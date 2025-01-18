import logging
import socket
import time


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TimeClient:
    """
    Client to connect to the atomic clock at NIST
    Note that requests should be limited to a maximum frequency of 4 seconds
    """
    def __init__(self):
        self.addr = "time.nist.gov"
        self.port = 37
    
    def get_atomic_time(self) -> int:
        """
        Time server returns seconds since 1900.
        It seems despite the cost of running the TCP socket they're begrudgingly
        maintaining it for 
        """
        s = socket.socket()
        s.connect((self.addr, self.port))
        d = s.recv(4)  # The server should return 4 bytes max
        return int.from_bytes(d)
    
    def get_system_time(self) -> int:
        """
        Unix systems have a time epoch of 1970, so need to offset the system
        clock by 70 years
        """
        epoch_time_offset = 2_208_988_800 # Seconds between 1900 & 1970
        return int(time.time()) + epoch_time_offset

    def print_times(self) -> None:
        atomic_time = self.get_atomic_time()
        system_time = self.get_system_time()
        logger.info(f"NIST time  : {atomic_time}")
        logger.info(f"System time: {system_time}")
        time.sleep(4)  # Hardcoding a rate limiter so you don't get blocked by the host


def main():
    time_client = TimeClient()
    time_client.print_times()


if __name__ == "__main__":
    main()
