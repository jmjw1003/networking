"""
Unrelated to the project but was reading about implementation prior ¯\\_(ツ)_/¯.
"""
class IPv4Conversion:
    @staticmethod
    def convert_readable_ip_to_numeric(addr: str | list[str] | list[int]) -> int:
        """
        Convert human readable IPv4 -> numeric representation
        """
        if isinstance(addr, str):
            addr = [int(i) for i in addr.split(".")]
        elif isinstance(addr[0], str):
            addr = [int(i) for i in addr]
        
        numeric_ip = 0
        for i in range(4):
            n = addr.pop()
            numeric_ip += (n << (8 * i))
        return numeric_ip
    
    @staticmethod
    def convert_numeric_ip_to_readable(addr: int) -> str:
        """
        Convert numerical representation of IPv4 -> human readable
        """
        nums = []
        for i in range(4):
            num = 0xff & addr >> (24 - (8 * i))
            nums.append(str(num))
        return ".".join(nums)

