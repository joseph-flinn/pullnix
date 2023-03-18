import argparse
import logging
import typing as t

from ..__about__ import __version__

from .list import command_list, create_list_subparser
#from .status import command_status, create_status_subparser
#from .refresh import command_refresh, create_refresh_subparser
#from .serve import command_serve, create_serve_subparser


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pullnix")
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(dest="subparser_name")

    list_parser = subparsers.add_parser("list", help="List configured NixOS Pull agents")
    create_list_subparser(list_parser)


    return parser


class CLINamespace(argparse.Namespace):
    log_level: "CLIVerbosity"
    subparser_name: "CLISubparserName"
    import_subparser_name: t.Optional["CLIImportSubparserName"]
    version: bool


ns = CLINamespace()


def cli(_args: t.Optional[t.List[str]] = None) -> None:
    parser = create_parser()
    args = parser.parse_args(_args, namespace=ns)

    if args.subparser_name is None:
        parser.print_help()
        return
    elif args.subparser_name == "list":
        command_list(parser=parser)
    elif args.subparser_name == "status":
        pass
    elif args.subparser_name == "refresh":
        pass
    elif args.sub_parser == "serve":
        pass

