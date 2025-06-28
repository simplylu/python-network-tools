__description__ = "Scan for ports on IP"
__help__ = "help for üprt"
__arguments__ = [
    {
        "short": "-i",
        "long": "--ip",
        "type": str,
        "help": "IP to check ports for",
        "required": True,
        "action": None
    },
    {
        "short": "-s",
        "long": "--start",
        "type": int,
        "help": "IP to start with",
        "required": False,
        "default": 1,
        "action": None
    },
    {
        "short": "-e",
        "long": "--end",
        "type": int,
        "help": "IP to end with",
        "required": False,
        "default": 1024,
        "action": None
    },
    {
        "short": "-t",
        "long": "--timeout",
        "type": int,
        "help": "Timeout for socket connection",
        "required": False,
        "default": 10,
        "action": None,
    },
    {
        "short": "-",
        "long": "--parallel",
        "type": int,
        "help": "Number of threads to spawn",
        "required": False,
        "default": 8,
        "action": None
    }
]


import concurrent.futures
import socket


def run(args):
    host = args.ip
    timeout = args.timeout or 10
    parallel = args.parallel or 8
    start = args.start or 1
    end = args.end or 1024
    ports = list(range(start, end + 1))
    open_ports = []

    def get_socket() -> socket.socket:
        s = socket.socket()
        s.settimeout(timeout)
        return s

    def check_port(ip: str, port: int) -> int:
        with get_socket() as s:
            try:
                s.connect((ip, port))
                return port
            except (socket.timeout, socket.error):
                return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:  # noqa: E501
        results = executor.map(check_port, [host]*len(ports), ports)
        open_ports = [port for port in results if port is not None]

    return {
        "host": host,
        "ports": ', '.join(map(str, open_ports))
    }
