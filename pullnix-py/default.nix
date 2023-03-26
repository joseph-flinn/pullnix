{ pkgs ? import <nixpkgs> {} }:
pkgs.callPackage ./derivation.nix {
  pkgs = pkgs;
  buildPythonApplication = pkgs.python310Packages.buildPythonApplication;
}
