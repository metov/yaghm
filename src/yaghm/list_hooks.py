"""
List hooks which are currently enabled in the repo.

# TODO: Support printing for only one hook type

Usage:
    list (-h | --help)
    list REPO
"""
from pathlib import Path

from docopt import docopt

from yaghm import log
from yaghm.lib import (
    hooks_path,
    VALID_HOOKS,
    require_repo_exists,
    render_wrapper,
    commands_path,
)


def main(argv):
    args = docopt(__doc__, argv=argv)

    log.debug(f"Arguments:\n{args}")

    prepo = Path(args["REPO"])
    require_repo_exists(prepo)

    for hook in VALID_HOOKS:
        phooks = hooks_path(prepo)

        pwrapper = phooks / hook
        if not pwrapper.exists():
            log.debug(f"No file at {pwrapper}")
            continue

        wrapper = pwrapper.read_text()
        if wrapper != render_wrapper(hook):
            log.warning(f"Ignoring unexpected script at {pwrapper}")
            continue

        pcmd = commands_path(phooks, hook)
        if not pcmd.exists():
            log.error(f"{pcmd} does not exist - {pwrapper} might be broken.")
            continue

        print(f"{hook}:\n{'='*(len(hook)+1)}\n{pcmd.read_text()}\n")
