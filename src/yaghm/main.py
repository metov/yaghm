"""
A minimal git hook manager. For details, see: https://www.github.com/metov/yaghm

Usage:
    yaghm (-h | --help)
    yaghm [--log LEVEL] enable [<args>...]
    yaghm [--log LEVEL] list [<args>...]
    yaghm [--log LEVEL] disable [<args>...]
    yaghm [--log LEVEL] CMDNAME [<args>...]

Options:
    --log LEVEL  Minimum level of logs to print [default: INFO]
"""
import logging

from docopt import docopt

from yaghm import log, enable, disable, list_hooks, custom_command


def main():
    args = docopt(__doc__, options_first=True)

    if level := args["--log"]:
        log.setLevel(logging.getLevelName(level.upper()))

    log.debug(f"Arguments:\n{args}")

    argv = args["<args>"]
    if args["enable"]:
        enable.main(argv)
    elif args["disable"]:
        disable.main(argv)
    elif args["list"]:
        list_hooks.main(argv)
    else:
        custom_command.main(args["CMDNAME"], argv)
