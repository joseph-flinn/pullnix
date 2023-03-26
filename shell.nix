with import <nixpkgs> {};
with pkgs;

let
  pullnix = pkgs.callPackage ./derivation.nix { 
    pkgs = pkgs;
  };
in mkShell {
  buildInputs = [
    pullnix
  ];
}
