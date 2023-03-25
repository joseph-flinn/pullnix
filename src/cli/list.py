import argparse
import typing as t


def create_list_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    return parser


def command_list(
    config: dict,
    parser: t.Optional[argparse.ArgumentParser] = None
) -> None:
    print(f"Running command: list")
    print(f"Config: {config}")

