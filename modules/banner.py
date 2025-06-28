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
    host = args.ip
    port = args.port
    timeout = args.timeout or 10
    try:
        s = socket.socket()
        s.settimeout(timeout)
        s.connect((host, port))
        banner = s.recv(1024).decode().strip()
        return {
            "host": args.ip,
            "port": args.port,
            "output": banner
        }
    except socket.error as e:
        return {
            "host": args.ip,
            "port": args.port,
            "error": str(e)
        }
    finally:
        s.close()
