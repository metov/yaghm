"""
Read a list of hooks from a config and enable them on the current repo.

You will be prompted if there is a complicated situation, eg. there's an
existing hook managed by another program or a hook is about to be removed,

Usage:
    enable (-h | --help)
    enable REPO [options]

Options:
    --conf PATH  Use given config instead of yaghm.yml in repo root
    --dryrun  Only echo what would have been done, don't actually do it
    -y  Non interactive mode, assume safe defaults instead of prompting user
"""
import subprocess
from pathlib import Path

import questionary
from docopt import docopt

from yaghm import log
from yaghm.lib import (
    hooks_path,
    VALID_HOOKS,
    require_repo_exists,
    render_wrapper,
    backup_path,
    commands_path,
    load_config,
)


def main(argv):
    args = docopt(__doc__, argv=argv)

    log.debug(f"Arguments:\n{args}")

    prepo = Path(args["REPO"])
    require_repo_exists(prepo)

    conf_override = args["--conf"]
    pconf = Path(conf_override) if conf_override else prepo / "yaghm.yml"
    config = load_config(pconf)

    dryrun = bool(args["--dryrun"])
    noask = bool(args["-y"])

    enable_hooks(prepo, config, dryrun, noask)


def enable_hooks(prepo, config, dryrun, noask):
    hooks = collect_hook_commands(config)
    for stage, hooks in hooks.items():
        make_wrapper(prepo, stage, dryrun)
        make_commands(prepo, stage, hooks, dryrun)


def collect_hook_commands(config):
    all_cmds = {}
    for hook in config:
        if hook not in VALID_HOOKS:
            log.warning(f"Skipping invalid hook: {hook}")
            continue

        cmds = all_cmds.setdefault(hook, [])
        for i in config[hook]:
            if isinstance(i, str):
                cmd = i
            elif isinstance(i, dict):
                cmd = i["enable"]
            else:
                log.warning(f"Ignoring unexpected type: {i}")
                continue

            cmds.append(cmd)

        log.debug(f"Collected {len(cmds)} {hook} hooks.")
    return all_cmds


def make_wrapper(prepo, stage, dryrun):
    phooks = hooks_path(prepo)
    pwrap = phooks / stage
    wrapper = render_wrapper(stage)

    if need_to_backup_wrapper(wrapper, pwrap):
        log.warning(f"There's an unexpected file at: {pwrap}")
        backup_wrapper(pwrap, dryrun)

    log.info(f"Writing wrapper at: {pwrap}")
    if not dryrun:
        pwrap.write_text(wrapper)
        subprocess.call(["chmod", "+x", str(pwrap)])


def need_to_backup_wrapper(wrapper, pwrap):
    if not pwrap.exists():
        log.debug(f"No existing {pwrap}")
        return False

    if pwrap.read_text() == wrapper:
        log.debug(f"Existing {pwrap} is already correct")
        return False

    return True


def backup_wrapper(pwrap, dryrun):
    pbackup = backup_path(pwrap)
    log.warning(f"It will be backed up to: {pbackup}")

    if pbackup.exists():
        msg = f"Overwrite old backup in {pbackup}?"
        if not questionary.confirm(msg, default=False).ask():
            log.critical(f"Can't write backup to {pbackup} because it already exists.")
            exit(1)

    if not dryrun:
        pwrap.rename(pbackup)


def make_commands(prepo, hook, newcmds, dryrun):
    pcmds = commands_path(hooks_path(prepo), hook)

    if pcmds.exists():
        oldcmds = set(s for s in pcmds.read_text().splitlines() if s != "")
        deleted = oldcmds - set(newcmds)
        if deleted:
            log.warning(f"{len(deleted)} hooks will be removed:\n" + "\n".join(deleted))
            if not questionary.confirm("Proceed?", default=True).ask():
                log.critical("Aborted on user request.")
                exit(1)

    log.debug(f"Writing command list to: {pcmds}")
    if not dryrun:
        pcmds.write_text("\n".join(newcmds))
