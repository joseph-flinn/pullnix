import argparse
import typing as t

from .utils import dicts2table, format_table

def create_list_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    return parser


def command_list(
    config: dict,
    parser: t.Optional[argparse.ArgumentParser] = None
) -> None:
    print(format_table(dicts2table(config["machines"]), has_header=True))

