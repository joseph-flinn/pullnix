import argparse
import typing as t
import uvicorn

from ..api.api import app


class CLIServeNamespace(argparse.Namespace):
    host: t.Optional[str]
    port: t.Optional[int]


def get_host(
    config: dict,
    args: CLIServeNamespace
) -> str:
    if args.host != "127.0.0.1":
        return args.host
    if "serve" in config and "host" in config["serve"]:
        return config["serve"]["host"]
    return "127.0.0.1"


def get_port(
    config: dict,
    args: CLIServeNamespace
) -> str:
    if args.port != 8000:
        return args.port
    if "serve" in config and "port" in config["serve"]:
        return config["serve"]["port"]
    return 8000


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
    config: dict,
    args: CLIServeNamespace,
    parser: t.Optional[argparse.ArgumentParser] = None
) -> None:
    uvicorn.run(app, host=get_host(config, args), port=get_port(config, args))
