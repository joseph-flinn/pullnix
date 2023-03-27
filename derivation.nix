{
  pkgs ? import <nixpkgs> {},
}:
let
  src_path = ./pullnix-sh;
  #pullnix = pkgs.writeShellScriptBin "pullnix" (builtins.readFile "${src_path}/pullnix");
in
pkgs.stdenv.mkDerivation {
  name = "pullnix";
  src = src_path;
  preConfigure = ''
    export PREFIX=$out
  '';
  installPhase = ''
    mkdir -p $out/bin
    cp $src/pullnix $out/bin
    cp $src/pullnix-switch $out/bin
    export PATH=$out/bin:$PATH
  '';
}
