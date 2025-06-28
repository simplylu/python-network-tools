import glob
import importlib
import argparse
import colorama
import json
import tabulate


def error(msg: str) -> None:
    """Method to print error messages in red

    Args:
        msg (str): The error message to print
    """
    print(f"{colorama.Fore.RED}{msg}{colorama.Fore.RESET}")


def create_modular_parser(modules: list) -> argparse.ArgumentParser:
    """Method to create an argument parser based on the modules config

    Args:
        modules (list): List of imported modules

    Returns:
        argparse.ArgumentParser: ArgumentParser with modular subcommands
    """
    # Create general ArgumentParser object and add a subparser object to it
    parser = argparse.ArgumentParser(description="A tool for different things")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Iterate over available modules
    for name, module in modules.items():
        # Read the mandatory and optional arguments from the modules
        arguments = module.__arguments__

        # Create a new subparser with the name of the module
        sub_parser = subparsers.add_parser(name, help=module.__description__)

        # Iterate over each argument defined in the module
        for argument in arguments:
            # Create a new argument for the subparser based on the module config
            sub_parser.add_argument(
                argument["short"],
                argument["long"],
                action=argument["action"],
                help=argument["help"],
                type=argument["type"],
                required=argument["required"],
                default=argument.get("default", ""))

    # Add general argument to define the output format
    parser.add_argument("-o", "--output", default="table", required=False, help="The format of your output", choices=["json", "csv", "tsv", "table"])  # noqa: E501

    return parser


def parse_modules() -> dict:
    # Create dict to store modules
    modules = dict()
    # Iterate over all available modules
    for module in glob.glob("modules/[!_]*.py"):
        # Extract the name from the module path
        name = module.split("/")[1].split(".")[0]
        # Import the module and map it to its name
        modules[name] = importlib.import_module(f".{name}", "modules")
    return modules


def main():
    # Import module to a dictionary
    modules = parse_modules()

    # Create an argument parser from the argument config in each module
    # and parse them to a Namespace
    parser = create_modular_parser(modules)
    args = parser.parse_args()

    # Run the selected module with the given args and store its output as JSON
    output = modules[args.command].run(args)

    # In case the error key exists, print the error and quit
    if "error" in output:
        error(output["error"])
        exit(1)

    # Check for the output format
    match args.output:
        case "table":
            # Format output and print it as table
            table = []
            for k, v in output.items():
                table.append([k, str(v)])
            print(tabulate.tabulate(table))
        case "json":
            # Print the output as formatted JSON
            print(json.dumps(output, indent=4))
        case "csv":
            # Print the output as CSV
            print(", ".join(output.keys()))
            print(", ".join(map(str, output.values())))
        case "tsv":
            # Print the output as TSV
            print("\t".join(output.keys()))
            print("\t".join(map(str, output.values())))
        case _:
            error("Unknown output format")
            exit(1)


if __name__ == "__main__":
    main()
