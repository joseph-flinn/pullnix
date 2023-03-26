import argparse
import json
import logging
import typing as t

from ..__about__ import __version__

from .list import command_list, create_list_subparser
from .status import CLIStatusNamespace, command_status, create_status_subparser
from .refresh import CLIRefreshNamespace, command_refresh, create_refresh_subparser
from .serve import CLIServeNamespace, command_serve, create_serve_subparser


def load_config(config: str) -> dict:
    with open(config, 'r') as config_file:
        return json.load(config_file)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pullnix")
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Configuration file for pullnix",
        default="pullnix.json"
    )

    subparsers = parser.add_subparsers(dest="subparser_name")

    list_parser = subparsers.add_parser("list", help="List configured NixOS Pull agents")
    create_list_subparser(list_parser)

    status_parser = subparsers.add_parser("status", help="Get status of a selected NixOS Pull system")
    create_status_subparser(status_parser)

    refresh_parser = subparsers.add_parser(
        "refresh",
        help="Force a NixOS Pull agent to sync with the target git repository"
    )
    create_refresh_subparser(refresh_parser)

    serve_parser = subparsers.add_parser("serve", help="start a NixOS Pull agent")
    create_serve_subparser(serve_parser)

    return parser


class CLINamespace(argparse.Namespace):
    log_level: "CLIVerbosity"
    subparser_name: "CLISubparserName"
    import_subparser_name: t.Optional["CLIImportSubparserName"]
    version: bool
    config: str


ns = CLINamespace()


def cli(_args: t.Optional[t.List[str]] = None) -> None:
    parser = create_parser()
    args = parser.parse_args(_args, namespace=ns)
    configs = load_config(args.config)

    if args.subparser_name is None:
        parser.print_help()
        return
    elif args.subparser_name == "list":
        command_list(
            configs,
            parser=parser
        )
    elif args.subparser_name == "status":
        command_status(
            configs,
            CLIStatusNamespace(**vars(args)),
            parser=parser
        )
    elif args.subparser_name == "refresh":
        command_refresh(
            configs,
            CLIRefreshNamespace(**vars(args)),
            parser=parser
        )
    elif args.subparser_name == "serve":
        command_serve(
            configs,
            CLIServeNamespace(**vars(args)),
            parser=parser
        )

