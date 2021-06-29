from distutils.core import setup

setup(
    name="yaghm",
    version="0.1.0",
    description="Minimal git hook manager for the command line.",
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
