"""
Run custom command (if defined) for each hook.

Usage:
    CMDNAME [options]

Options:
    --conf PATH  Use given config instead of yaghm.yml in current working directory
    --dryrun  Only echo what would have been done, don't actually do it
"""
import subprocess
from pathlib import Path

from docopt import docopt

from yaghm import log
from yaghm.lib import VALID_HOOKS, load_config


def main(command_name, argv):
    args = docopt(__doc__, argv=argv)

    log.debug(f"Arguments:\n{args}")

    pconf = Path(args["--conf"] or "yaghm.yml")
    config = load_config(pconf)

    for hook in VALID_HOOKS:
        if hook not in config:
            log.debug(f"No {hook} hook defined, skipping.")
            continue

        cmds = config[hook]
        for c in cmds:
            if not isinstance(c, dict):
                log.info(f"No {command_name} defined for: {c}")
                continue

            if command_name not in c:
                log.info(f"No {command_name} defined for: {c['enable']}")
                continue

            cmd = c[command_name]
            if not args["--dryrun"]:
                res = subprocess.run(cmd, shell=True).returncode
            else:
                print(f"Pretending to run: {cmd}")
                res = 0

            if res == 0:
                log.info(f"Command successful: {cmd}")
            else:
                log.error(f"Command failed: {cmd}")
