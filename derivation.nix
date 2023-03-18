{ pkgs, buildPythonApplication }:
with pkgs.python310Packages;
buildPythonApplication rec {
  name = "pullnix-${version}";
  version = "0.0.1";

  src = ./.;

  buildInputs = [ pytest black ];
  propagatedBuildInputs = [ fastapi uvicorn ];

  doCheck = false;

}
