"""
Disable hooks by deleting the wrapper.

Usage:
    disable (-h | --help)
    disable REPO [options]

Options:
    --dryrun  Only echo what would have been done, don't actually do it.
    -y  Non interactive mode, assume safe defaults instead of prompting user
"""
from pathlib import Path

from docopt import docopt

from yaghm import log
from yaghm.lib import (
    require_repo_exists,
    render_wrapper,
    VALID_HOOKS,
    backup_path,
    hooks_path,
)


def main(argv):
    args = docopt(__doc__, argv=argv)

    log.debug(f"Arguments:\n{args}")

    prepo = Path(args["REPO"])
    require_repo_exists(prepo)

    dryrun = bool(args["--dryrun"])
    noask = bool(args["-y"])

    disable_hooks(prepo, dryrun, noask)


def disable_hooks(prepo, dryrun, noask):
    for hook in VALID_HOOKS:
        wrapper = render_wrapper(hook)
        pwrap = hooks_path(prepo) / hook

        if not pwrap.exists():
            continue

        if wrapper != pwrap.read_text():
            log.warning(f"Skipping unexpected file at: {pwrap}")
            continue

        log.info(f"Deleting: {pwrap}")
        pback = backup_path(pwrap)
        if pback.exists():
            log.info(f"Restoring from backup: {pback}")
            if not dryrun:
                backup_path(pwrap).rename(pwrap)
        else:
            if not dryrun:
                pwrap.unlink()
