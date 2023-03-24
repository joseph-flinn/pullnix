def sync() -> bool:
    # Get latest HEAD
    remote_head = None
    local_head = "changed"

    print(f"Checking remote head")
    if remote_head != local_head:# IF latest HEAD != local HEAD
        #git.pull(dest=config_dir)
        print(f"pulling new config: {remote_head}")
        return False

    return True
