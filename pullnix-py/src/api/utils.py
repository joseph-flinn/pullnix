import typing as t
import subprocess


def run_shell(command: str, return_output=False) -> t.Optional[str]:
    result = subprocess.run(command.split(" "), capture_output=True)
    if result.returncode != 0:
        raise Exception(f"[!] `{command}` failed")

    if return_output:
        return result.stdout
    return None

