with import <nixpkgs> {};
with pkgs.python310Packages;

let
  pullnix = pkgs.callPackage ./derivation.nix { 
    pkgs = pkgs;
    buildPythonApplication = buildPythonApplication; 
  };
  pythonEnv = with pkgs.python310Packages; [
    black
    pytest
    pytest-asyncio
  ];
in mkShell {
  buildInputs = [
    pythonEnv
    pullnix
  ];
}
