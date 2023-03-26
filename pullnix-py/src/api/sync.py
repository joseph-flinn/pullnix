import typing as t

from src.api.utils import run_shell


def sync(config: dict) -> t.Tuple[bool, str]:
    # Get latest HEAD
    def get_git_head(branch: str) -> str:
        return str(run_shell(f"git rev-parse {branch}", return_output=True), "UTF-8").strip("\n")

    run_shell("git fetch")
    local_head = get_git_head(config["git"]["branch"])
    remote_head = get_git_head(f"{config['git']['remote']}/{config['git']['branch']}")

    print(f"Local HEAD: {local_head}\nRemote HEAD: {remote_head}")
    if remote_head != local_head:
        print(f"pulling new config: {remote_head}")
        run_shell("git pull")
        return (False, remote_head)

    return (True, remote_head)
