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


def has_required_git_configs(git_config: dict, keys: list) -> bool:
    for key in keys:
        if key not in git_config:
            return False
    return True


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
    parser.add_argument(
        "--check-vuln",
        action="store_true",
        help="Use vulnix as an additional check before switching to the newest build"
    )

    return parser


def command_serve(
    config: dict,
    args: CLIServeNamespace,
    parser: t.Optional[argparse.ArgumentParser] = None
) -> None:
    required_git_configs = ["owner", "repo", "remote", "branch"]
    if "git" in config and has_required_git_configs(config["git"], required_git_configs):
        app.config = config
        app.config["check-vuln"] = args.check_vuln
        uvicorn.run(app, host=get_host(config, args), port=get_port(config, args))
    else:
        print(f"[!] missing required git configs: {', '.join(required_git_configs)}")

