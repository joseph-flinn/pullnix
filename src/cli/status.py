import argparse
import typing as t


class CLIStatusNamespace(argparse.Namespace):
    host: t.Optional[str]
    port: t.Optional[int]


def create_status_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    return parser


def command_status(
    args: CLIStatusNamespace,
    parser: t.Optional[argparse.ArgumentParser] = None
) -> None:
    print("Running command: status")

