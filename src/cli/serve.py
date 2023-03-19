import argparse
import typing as t
import uvicorn

from ..api.api import app


class CLIServeNamespace(argparse.Namespace):
    host: t.Optional[str]
    port: t.Optional[int]


def create_serve_subparser(
    parser: argparse.ArgumentParser,
) -> argparse.ArgumentParser:
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="port to run the agent on"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="host address to run the agent on (default: 127.0.0.1)"
    )

    return parser


def command_serve(
    args: CLIServeNamespace,
    parser: t.Optional[argparse.ArgumentParser] = None
) -> None:
    uvicorn.run(app, host=args.host, port=args.port)
