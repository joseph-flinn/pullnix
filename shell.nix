#with import <nixpkgs> {};
#let
#  pythonEnv = python310.withPackages(ps: with ps; [
#    fastapi
#    uvicorn
#
#    black
#    pytest
#  ]);
#  myProject = pkgs.callPackage ./derivation.nix {};
#in mkShell {
#  packages = [
#    pythonEnv
#    myProject
#  ];
#}

with import <nixpkgs> {};
with pkgs.python310Packages;

let
  pullnix = pkgs.callPackage ./derivation.nix { 
    pkgs = pkgs;
    buildPythonApplication = buildPythonApplication; 
  };
in mkShell {
  buildInputs = [
    pullnix
  ];
}
