with import <nixpkgs> {};
let
  pythonEnv = python310.withPackages(ps: [

    ps.black
    ps.pytest
  ]);
in mkShell {
  packages = [
    pythonEnv
  ];
}
