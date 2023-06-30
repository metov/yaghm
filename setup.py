from distutils.core import setup
from pathlib import Path

from setuptools import find_packages

setup(
    name="yaghm",
    version="0.3.1",
    description="Minimal git hook manager for the command line.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://www.github.com/metov/yaghm",
    author="Azat Akhmetov",
    author_email="azatinfo@yandex.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["templates/*"]},
    install_requires=[
        "coloredlogs",
        "docopt",
        "GitPython",
        "Jinja2",
        "PyYAML",
        "questionary",
        "ruamel.yaml",
    ],
    entry_points={
        "console_scripts": [
            "yaghm=yaghm.main:main",
        ],
    },
)
