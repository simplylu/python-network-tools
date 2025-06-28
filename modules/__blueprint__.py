__description__ = "Short description for argparse"
__arguments__ = [
    {
        "short": "-i",
        "long": "--ip",
        "type": str,
        "help": "IP to grab banner from",
        "required": True,
        "default": "default value",  # not required
        "action": None
    }
]


def run(args):
    print("Banner")
