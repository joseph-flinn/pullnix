import argparse
import typing as t


class CLIStatusNamespace(argparse.Namespace):
    target: t.Optional[str]


def create_status_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    parser.add_argument(
        "--target",
        type=str,
        help="NixOS agent to send the status request to"
    )

    return parser


def command_status(
    args: CLIStatusNamespace,
    parser: t.Optional[argparse.ArgumentParser] = None
) -> None:
    if args.target:
        print(f"Command: status\nTarget: {args.target}")
    else:
        print(f"Command: status\nTarget: all")
