# pullnix

## Design

We need to do a bare metal install of NixOS with pixiecore. The initial config will include:
  - the pullnix
  - A git repo deploy key to pull the rest of the configuratin from
  - an authorized SSH key for remote login


Once the pullnix is running, it will poll the repo every 5 minutes for a configuration update


## pullnix 

- pull deploy from git repo (think pull deployments in ArgoCD)
- build validation (script to load from repo. If fails, revert to previous generation)
    + see https://github.com/Infinisil/nixus for example of rollback
- Run a `vulnix` on the build directory before attempting to switch if `--check-vuln` is configured for the operator


## Development
### Requirements
- NixPkgs
- `nix-shell`
- `nixos-generate-config`
- `nixos-rebuild`


### Run

```
# Load development environment
nix-shell

# Run the application in development mode
pullnix --version
```

**Note:** I couldn't get the develop mode working with Nix...so every change has to be rebuilt by
exiting `nix-shell` and re-entering it


### Testing
#### Initial Setup
Before local testing, we need hardware specific configurations to test builds with
```
cd tests/fixtures/nixos-configs
nixos-generate-configs --dir .
```

### TODO
#### Phases

- **MVP:** Agent that polls git and builds/switches and auto rolls back if it can no longer access git repo
- **Phase 1:** Rebuild logging and add remote logging
- **Phase 2:** Set up dashboard backed from centralized logging system
- **Phase 3:** Add in vulnerability checking logic


#### List

- [ ] POC with bash + [systemd](https://stackoverflow.com/questions/58243712/how-to-install-systemd-service-on-nixos)
- [ ] Rip out FastAPI and convert to just a long running process
- [ ] Add git check to see if the agent should rollback
- [ ] Package for deployment on NixOS
- [ ] Add in vulnerability checking
