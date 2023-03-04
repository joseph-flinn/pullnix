# pullnix

## Design

We need to do a bare metal install of NixOS with pixiecore. The initial config will include:
  - the pullnix
  - A git repo deploy key to pull the rest of the configuratin from
  - an authorized SSH key for remote login


Once the pullnix is running, it will poll the repo every 5 minutes for a configuration update


## pullnix Features

- pull deploy from git repo (think pull deployments in ArgoCD)
- build validation (script to load from repo. If fails, revert to previous generation)
    + see https://github.com/Infinisil/nixus for example of rollback
- provide api for status (There definitely should be authentication for the api)
- Run a `vulnix` on the build directory before attempting to switch if `secure` is configured for the operator


## CLI tool - `nixctl`

| command + options | description |
| ----------------- | ----------- |
| `list` | lists all of the machines currently being tracked by `nixctl` |
| `status --all` | Get the status of all of the machines currently being tracked |
| `status <target>` | Get the status of all of the machines currently being tracked |
| `refresh --all` | Force all operators to check for updates in the git repo |
| `refresh <target>` | Force all operators to check for updates in the git repo |


This could be a shell script that wraps ansible playbooks; similar to `homelab`. This approach 
would work well if pixiecore is ran with ansible similar to https://github.com/khuedoan/homelab.
This would also remove the requirement for a public api on each node. It could be constrained to
only a localhost api that could be hit from SSH

