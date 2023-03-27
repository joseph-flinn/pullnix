# pullnix

:warning: **TL;DR:** This doesn't work 

## Idea

I've been working the kubernetes environment for a few years. GitOps has introduced a new way of
thinking about deployments; pull deploys vs push deploys. With the declarative nature of NixOS and the 
heavy use of git in the community, I thought it'd be interesting to see if pull deploys could be 
possible for NixOS to increase security by not requiring SSH access to the edge device.

I could see the advantage of an edge device being flashed with NixOS that contained a GitHub Deploy Key
to phone home to auto update. All of the OS updates/changes would be fully auditable via the git repo. I
could also see this being helpful for those of us (me) that would like updates to be automated, but in a
way that could be rolled back in a programmatic way if a verification step failed.


## Design

The overall design 2.0 (limiting scope to strictly MVP for speed of idea testing) is to run a bash script 
as a systemd service. This service would be deployed to a machine already running NixOS (or theoretically 
a part of the initial `configuration.nix` build/install). 

The MVP design assumes that `/etc/nixos` is a git repository with a symlink for `configuraion.nix`. 

Once pullnix is running, it will poll the repo every 5 minutes for a configuration update, if it is out
of sync, pull the newest configuration and switch. If the switch somehow disrupts communication with git, 
switch back. 

If this all works, it'd be an interesting idea to run `vulnix` against the `result` file before switching
to run some sort of logic to measure if the new build is more vulnerable than the current one.


## Implementation

After a few hours, I had a bash script that had the git polling working pretty well. It was accurately 
alerting me to when the repo was out of sync, would update the local version, successfully build the new
version, then it would print that it would be running `nixos-switch` if it was enabled and not just the 
`echo` command. 

<details><summary><i>code snippet</i></summary>
<p>

```bash
# bin/pullnix

NIXOS_CONFIG_DIR=/etc/nixos
LOG_DIR=/var/log/pullnix
PULLNIX_LOG=$LOG_DIR/pullnix.log
GIT_REMOTE=origin
GIT_BRANCH=main

#POLL_TIME=300
POLL_TIME=30


# Set up logging files
echo "=====Setting up pullnix====="
if ! [ -d $LOG_DIR ]; then
    echo "Creating $LOG_DIR"
    mkdir $LOG_DIR
fi
if ! [ -f $PULLNIX_LOG ]; then
    echo "Creating $PULLNIX_LOG"
    touch $PULLNIX_LOG
fi

echo "NIX_PATH: $NIX_PATH"
echo "PATH: $PATH"
echo "============================"


runSync() {
    git pull
    echo "> nixos-rebuild build"
    nixos-rebuild build -p $remote_head -I $NIXOS_CONFIG_DIR/configuration.nix

    if [ $? -eq 0 ]; then
        echo "> nixos-rebuild switch" >> $PULLNIX_LOG
        #nixos-rebuild switch -p $remote_head -I $NIXOS_CONFIG_DIR/configuration.nix >> $PULLNIX_LOG 2>&1

        if [ $(git ls-remote &>> /dev/null; echo $?) -eq 0 ]; then
            echo "git repo connection successful" >> $PULLNIX_LOG
        else
            echo "git repo connection failed" >> $PULLNIX_LOG
            echo "Switching back" >> $PULLNIX_LOG
            #nixos-rebuild switch --rollback >> $PULLNIX_LOG 2>&1
        fi
    fi
}


cd $NIXOS_CONFIG_DIR

while true; do
    git fetch
    local_head=$(git rev-parse $GIT_BRANCH)
    remote_head=$(git rev-parse $GIT_REMOTE/$GIT_BRANCH)

    if [ $local_head != $remote_head ]; then
        echo "Out of sync -- local:${local_head:0:7} => remote:${remote_head:0:7}"
        runSync
    fi

    sleep $POLL_TIME
done
```

</p>
</details>


I then spent the next few hours running around being a NixOS noob and trying to figure out how make a 
derivation of the bash script. While I could have added the contents of this repo as files in my 
`nixos-configs` repo under a subdirectory of `./pkgs`, I was stubborn and wanted to pull in the package
from a git repo.


I finally got them working (seen as the *.nix files
[joseph-flinn/pullnix](https://github.com/joseph-flinn/pullnix.git))! Looking back, it probably would
have been a lot easier to just add a derivation directly in the `./pkgs` directory. Every time I updated
`pullnix`, I then had to update the `fetchGitHub` sha and rev


<details><summary><i>code snippet</i></summary>
<p>

```bash
# nixos-configs/pkgs/pullnix/default.nix

{ stdenv, fetchFromGitHub, bash}:

stdenv.mkDerivation rec {
  name = "pullnix-${version}";
  version = "a77dcea124f79fe9b88e54cb52b8f12d53768370";

  src = fetchFromGitHub {
    owner = "joseph-flinn";
    repo = "pullnix";
    rev = "${version}";
    sha256 = "0sgnzvynnh1z95avwrfn0r1y9zb8kpaph9hqd9fn2qvfx01mifai";
  };

  buildInputs = [ bash ];
  preConfigure = ''
    export PREFIX=$out
  '';
}
```

```nix
# configuration.nix 

{ config, pkgs, ... }:
let
  pullnix = pkgs.callPackage ../pkgs/pullnix {};
in
{
  #...
  environment.systemPackages = with pkgs; [
     "${pullnix}"
  ];

```
</p>
</details>


After getting the bash script installed as an executable in the nix store, I enabled the 
`nixos-rebuild switch` and tested that the logic worked altogether by manually running the script. 
So far so good. On to enabling the service via `systemd`.

I ran into some issues translating between systemd configuration and systemd the nix-way. Long story
short, full paths are important in systemd and bash scripts need a shebang or to be explicitly run. In
addition to that, PATH didn't have `/run/current-system/sw/bin` in it for `git`, and `ssh` (needed for 
`git`). Thinking that `Environment="PATH=/run/current-system/sw/bin:${PATH}"` would work, I messed around
with this format for a bit. Turns out that this doesn't work in non-NixOS environments either. I ended up
just hardcoding the paths for both `PATH` and `NIX_PATH`.


<details><summary><i>code snippet</i></summary>
<p>


```nix
# configuration.nix

{
  #...

  systemd.services.pullnix = {
    enable = true;
    description = "pullnix agent";
    after = ["network.target"];
    serviceConfig = {
      Type = "simple";
      Restart = "always";
      RestartSec = 5;
      Environment = "PATH=/run/current-system/sw/bin NIX_PATH=/root/.nix-defexpr/channels:nixpkgs=/nix/var/nix/profiles/per-user/root/channels/nixos:nixos-config=/etc/nixos/configuration.nix:/nix/var/nix/profiles/per-user/root/channels";
      ExecStart = "${pkgs.bash}/bin/bash ${pullnix}/bin/pullnix";

      StandardOutput = "append:/var/log/pullnix/pullnix.log";
      StandardError = "append:/var/log/pullnix/pullnix.log";
    };
    wantedBy = [ "multi-user.target" ];
  };

  #...
```

</p>
</details>



Everything seemed to be humming along quite nicely. Until...until I did a full test where I was expecting
the system to switch itself. The agent did exactly what it was supposed until `nixos-rebuild switch` got
to the stage where it restarts services. `pullnix` was terminated in the middle of the switch. The switch 
was being run in the `pullnix` process so it was also terminated before it completed and brought the new
`pullnix` back up. The next step was to fork the switch process and verification to outside of the process
that would be terminated on restart.


<details><summary><i>code snippet</i></summary>
<p>


```bash
# bin/pullnix

NIXOS_CONFIG_DIR=/etc/nixos
LOG_DIR=/var/log/pullnix
PULLNIX_LOG=$LOG_DIR/pullnix.log
GIT_REMOTE=origin
GIT_BRANCH=main

#POLL_TIME=300
POLL_TIME=30


# Set up logging files
echo "=====Setting up pullnix====="
if ! [ -d $LOG_DIR ]; then
    echo "Creating $LOG_DIR"
    mkdir $LOG_DIR
fi
if ! [ -f $PULLNIX_LOG ]; then
    echo "Creating $PULLNIX_LOG"
    touch $PULLNIX_LOG
fi

echo "NIX_PATH: $NIX_PATH"
echo "PATH: $PATH"
echo "============================"


runSync() {
    git pull
    echo "> nixos-rebuild build"
    nixos-rebuild build -p $remote_head -I $NIXOS_CONFIG_DIR/configuration.nix

    if [ $? -eq 0 ]; then
        pullnix-switch $NIX_CONFIG_DIR $PULLNIX_LOG $remote_head &
    fi
}


cd $NIXOS_CONFIG_DIR

while true; do
    git fetch
    local_head=$(git rev-parse $GIT_BRANCH)
    remote_head=$(git rev-parse $GIT_REMOTE/$GIT_BRANCH)

    if [ $local_head != $remote_head ]; then
        echo "Out of sync -- local:${local_head:0:7} => remote:${remote_head:0:7}"
        runSync
    fi

    sleep $POLL_TIME
done
```

```bash
# bin/pullnix-switch

NIX_CONFIG_DIR=$0
PULLNIX_LOG=$1

remote_head=$2


echo "====="
echo "PATH: $PATH"
echo "NIX_PATH: $NIX_PATH"
echo "NIX_CONFIG_DIR: $NIX_CONFIG_DIR"
echo "PULLNIX_LOG: $PULLNIX_LOG"
echo "remote_head: $remote_head"
echo "====="


cd $NIX_CONFIG_DIR 

echo "> nixos-rebuild switch" >> $PULLNIX_LOG
nixos-rebuild switch -p $remote_head -I $NIXOS_CONFIG_DIR/configuration.nix >> $PULLNIX_LOG 2>&1

if [ $(git ls-remote &>> /dev/null; echo $?) -eq 0 ]; then
    echo "git repo connection successful" >> $PULLNIX_LOG
else
    echo "git repo connection failed" >> $PULLNIX_LOG
    echo "Switching back" >> $PULLNIX_LOG
    nixos-rebuild switch --rollback >> $PULLNIX_LOG 2>&1
fi
```
</p>
</details>


This seemed to work on initial testing. `pullnix` was staying up on `nixos-build`, which means that 
it could continue working, but...it wouldn't restart itself which means that it couldn't manage itself.
While this might not have been a big issue if it was managed outside of the NixOS configuration, that 
breaks the entire philosophy of Nix. 


## Future Work
I'd like to see something like this idea in the future. However, I have realized that there is a problem
with having systemd, managed by NixOS, trying to then manage NixOS where NixOS will kill it and its 
processes on reload. Something is needed outside of NixOS but...still on the machine?

If this is possible, more learning of NixOS and how it operates is needed. For now, I'll be using one
of the other ops tools: [NixOps](https://github.com/NixOS/nixops), 
[deploy-rs](https://github.com/serokell/deploy-rs), [morph](https://github.com/DBCDK/morph), or 
[nixus](https://github.com/infinisil/nixus/tree/master)

