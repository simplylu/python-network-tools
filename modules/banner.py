__description__ = "Grab a banner from ip:port"
__arguments__ = [
    {
        "short": "-i",
        "long": "--ip",
        "type": str,
        "help": "IP to grab banner from",
        "required": True,
        "action": None
    },
    {
        "short": "-p",
        "long": "--port",
        "type": int,
        "help": "Port for the service to grab banner from",
        "required": True,
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
    }
]

import socket


def run(args):
    # Store values from parsed arguments
    host = args.ip
    port = args.port
    timeout = args.timeout or 10
    try:
        # Create socket and connect to host:port
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((host, port))
        # Receive data from service
        banner = s.recv(1024).decode().strip()
        # Return data as JSON
        return {
            "host": args.ip,
            "port": args.port,
            "output": banner
        }
    except socket.error as e:
        # Return error in case the connection fails
        return {
            "host": args.ip,
            "port": args.port,
            "error": str(e)
        }
    finally:
        # Close the socket in any case
        s.close()
