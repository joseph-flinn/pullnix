from time import sleep


def build():
    #os.system("nixos-rebuild build")
    print("running: nixos-rebuild build")


def vulnix() -> bool:
    #os.system("vulnix result")
    print("running: vulnix")


def switch():
    def verify_switch():
        print(f"Verifying switch")
        sleep(30)
        #success = os.system("ssh") works

        success = True
        if not success:
            os.system("nixos-rebuild switch --rollback")

    #os.system("nixos-rebuild switch")
    print("running: nixos-rebuild switch")
    verify_switch()


