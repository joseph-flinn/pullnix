{ lib, python3Packages }:
with python3Packages;
buildPythonApplication {
  pname = "pullnix";
  version = "0.1";

  propagatedBuildInputs = [ fastapi pytest ];

  src = ./.;
}
