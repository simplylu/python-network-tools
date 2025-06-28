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
    # Retrieve values from ArgumentParser
    host = args.ip
    timeout = args.timeout or 10
    parallel = args.parallel or 8
    start = args.start or 1
    end = args.end or 1024

    # Create a list of ports to scan
    ports = list(range(start, end + 1))

    # Create a list to store open ports in
    open_ports = []

    def get_socket() -> socket.socket:
        """Function to create socket with predefined timeout

        Returns:
            socket.socket: Socket
        """
        s = socket.socket()
        s.settimeout(timeout)
        return s

    def check_port(ip: str, port: int) -> int:
        """Method to check if port is open on IP

        Args:
            ip (str): IP address of the server to scan
            port (int): The port to check for

        Returns:
            int: Port if it is open, else None
        """
        with get_socket() as s:
            # Try to connect to IP on port and return the port
            # if the connection was successful
            try:
                s.connect((ip, port))
                return port
            except (socket.timeout, socket.error):
                # Return nothing if the connection failed
                return None

    # Magic to concurrently run X threads to scan the ports in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:  # noqa: E501
        # Store result from every threads
        results = executor.map(check_port, [host]*len(ports), ports)
        # Filter out None results
        open_ports = [port for port in results if port is not None]

    # Return results as JSON
    return {
        "host": host,
        "ports": ', '.join(map(str, open_ports))
    }
