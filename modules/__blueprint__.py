# This description will be used within the ArgumentParser
__description__ = "Short description for argparse"

# This is the config for mandatory and optional arguments used by this module
__arguments__ = [
    {
        # Short argument in the CLI
        "short": "-i",
        # Long argument in the CLI
        "long": "--ip",
        # This will be the type when being accessed from the Namespace
        "type": str,
        # The help text shown when calling the help for the main script
        "help": "IP to grab banner from",
        # If the argument is required or not
        "required": True,
        # The default value if not set, not required
        "default": "default value",
        # None if the value should be stored, "store_true" if it acts as a flag
        "action": None
    }
]


def run(args):
    """The function that runs the code of the module

    Args:
        args (Namespace): The argument namespace returned from the ArgumentParser
    """
    print("Banner")
