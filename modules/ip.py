__description__ = "Track IP"
__help__ = "help for ip"
__arguments__ = [
    {
        "short": "-i",
        "long": "--ip",
        "type": str,
        "help": "IP to track",
        "required": True,
        "action": None
    }
]

import requests


def run(args):
    ip = args.ip
    try:
        res = requests.get(f"https://ipinfo.io/{ip}").json()
        return {
            "ip": ip,
            "output": f"{res['country']}, {res['city']}, {res['org']}"
        }
    except Exception as e:
        return {
            "ip": ip,
            "error": str(e)
        }
