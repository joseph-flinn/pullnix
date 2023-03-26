import argparse
import json
import logging
import typing as t

from ..__about__ import __version__

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
    elif args.subparser_name == "serve":
        command_serve(
            configs,
            CLIServeNamespace(**vars(args)),
            parser=parser
        )

