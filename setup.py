from distutils.core import setup
from pathlib import Path

setup(
    name="yaghm",
    version="0.1.2",
    description="Minimal git hook manager for the command line.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://www.github.com/metov/yaghm",
    author="Azat Akhmetov",
    author_email="azatinfo@yandex.com",
    package_dir={"": "src"},
    install_requires=[
        "coloredlogs",
        "docopt",
        "GitPython",
        "Jinja2",
        "PyYAML",
        "questionary",
    ],
    entry_points={
        "console_scripts": [
            "yaghm=yaghm.main:main",
        ],
    },
)
