import glob
import importlib
import argparse
import colorama
import json
import tabulate


def error(msg: str) -> None:
    print(f"{colorama.Fore.RED}{msg}{colorama.Fore.RESET}")


def create_modular_parser(modules: list) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="A tool for different things")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, module in modules.items():
        arguments = module.__arguments__
        sub_parser = subparsers.add_parser(name, help=module.__description__)
        for argument in arguments:
            sub_parser.add_argument(
                argument["short"],
                argument["long"],
                action=argument["action"],
                help=argument["help"],
                type=argument["type"],
                required=argument["required"],
                default=argument.get("default", ""))

    parser.add_argument("-o", "--output", default="table", required=False, help="The format of your output", choices=["json", "csv", "tsv", "table"])  # noqa: E501
    return parser


def parse_modules() -> dict:
    modules = dict()
    for module in glob.glob("modules/[!_]*.py"):
        name = module.split("/")[1].split(".")[0]
        modules[name] = importlib.import_module(f".{name}", "modules")
    return modules


def main():
    modules = parse_modules()
    parser = create_modular_parser(modules)
    args = parser.parse_args()

    output = modules[args.command].run(args)
    if "error" in output:
        error(output["error"])
        exit(1)

    match args.output:
        case "table":
            table = []
            for k, v in output.items():
                table.append([k, str(v)])
            print(tabulate.tabulate(table))
        case "json":
            print(json.dumps(output, indent=4))
        case "csv":
            print(", ".join(output.keys()))
            print(", ".join(map(str, output.values())))
        case "tsv":
            print("\t".join(output.keys()))
            print("\t".join(map(str, output.values())))
        case _:
            print("")


if __name__ == "__main__":
    main()
