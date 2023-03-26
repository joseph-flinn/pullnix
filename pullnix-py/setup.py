from setuptools import setup, find_packages

from src.__about__ import __version__

setup(
    name="pullnix",
    version=f"{__version__}",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'pullnix = src.cli:cli',
        ]
    }
)
