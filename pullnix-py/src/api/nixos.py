import subprocess

from time import sleep

from src.api.utils import run_shell


def build(commit_hash, nixos_dir="./") -> bool:
    try:
        print(f"running: nixos-rebuild build")
        run_shell(f"nixos-rebuild build -p {commit_hash[:7]} -I {nixos_dir}/configuration.nix")
    except Exception as e:
        print(e)
        return False
    return True


def vulnix() -> bool:
    try:
        print(f"running: vulnix")
        run_shell(f"vulnix result")
    except Exception as e:
        print(e)
        return False
    return True


def switch() -> bool:
    print("running: nixos-rebuild switch")
    #run_shell("nixos-rebuild test")
    #print(f"Verifying new system")

    #success = True
    ##success = os.system("ssh") works

    #if success:
    #    run_shell("nixos-rebuild switch")
    #else:
    #    run_shell("nixos-rebuild --rollback switch")
    #return success


