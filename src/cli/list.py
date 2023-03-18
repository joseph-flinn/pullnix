import argparse
import typing as t


def create_list_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    return parser


def command_list(parser: t.Optional[argparse.ArgumentParser] = None) -> None:
    print("Running command: list")

