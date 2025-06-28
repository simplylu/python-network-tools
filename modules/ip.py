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
    # Retrieve values from given arguments
    ip = args.ip
    try:
        # Request ipinfo.io to get basic IP information
        res = requests.get(f"https://ipinfo.io/{ip}")

        # Check if response is OK
        if res.status_code // 100 != 2:
            raise Exception()

        # Get JSON from response
        data = res.json()
        # Return results as JSON
        return {
            "ip": ip,
            "output": f"{data['country']}, {data['city']}, {data['org']}"
        }
    except Exception as e:
        # Return error in case something went wrong
        return {
            "ip": ip,
            "error": str(e)
        }
