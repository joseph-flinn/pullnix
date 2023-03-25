import os
import subprocess

from src.api.nixos import build, vulnix, switch


def test_build():
    assert build("./tests/fixtures/nixos")
