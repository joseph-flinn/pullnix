import os
import subprocess

from time import sleep


def build(nixos_dir="./nixos") -> bool:
    print("running: nixos-rebuild build")
    result = subprocess.run("nixos-rebuild build".split(" "))

    if result.returncode != 0:
        return False
    return True


def vulnix() -> bool:
    #os.system("vulnix result")
    result = subprocess.run("vulnix result".split(" "))

    if result.returncode != 0:
        return False
    return True


def switch(switch_time: int = 30) -> bool:
    def verify_switch() -> bool:
        print(f"Verifying switch")
        sleep(switch_time)
        #success = os.system("ssh") works

        success = True
        if not success:
            os.system("nixos-rebuild switch --rollback")

        return success

    #os.system("nixos-rebuild switch")
    print("running: nixos-rebuild switch")
    return verify_switch()


