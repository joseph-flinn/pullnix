import argparse
import os
import typing as t


class CLIRefreshNamespace(argparse.Namespace):
    target: t.Optional[str]
    all: t.Optional[bool]


def create_refresh_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    parser.add_argument(
        "--target",
        type=str,
        help="NixOS agent to send the refresh request to"
    )
    parser.add_argument(
        "--all",
        action="store_const",
        default=False,
        const=True
    )

    return parser


def command_refresh(
    args: CLIRefreshNamespace,
    parser: t.Optional[argparse.ArgumentParser] = None
) -> None:
    if args.target and args.all:
        print(f"Cannot use both <target> and --all")
        os.exit(1)
    elif args.target:
        print(f"Command: refresh\nTarget: {args.target}")
    elif args.all:
        print(f"Command: refresh\nTarget: all")
    else:
        print(f"Please specific either <target> or set --all")
        os.exit(1)

