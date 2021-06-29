# From https://githooks.com/#how-do-git-hooks-work
from pathlib import Path

from jinja2 import Environment, PackageLoader

from yaghm import log

VALID_HOOKS = [
    "applypatch-msg",
    "pre-applypatch",
    "post-applypatch",
    "pre-commit",
    "prepare-commit-msg",
    "commit-msg",
    "post-commit",
    "pre-rebase",
    "post-checkout",
    "post-merge",
    "pre-receive",
    "update",
    "post-receive",
    "post-update",
    "pre-auto-gc",
    "post-rewrite",
    "pre-push",
]


def require_repo_exists(prepo):
    if prepo.exists():
        return

    log.critical(f"Path does not exist: {prepo}")
    exit(1)


def render_wrapper(stage):
    env = Environment(loader=PackageLoader("yaghm"))
    template = env.get_template("wrapper.jinja2")
    return template.render(stage=stage)


def hooks_path(prepo) -> Path:
    return prepo / ".git/hooks"


def backup_path(wrapper_path):
    return Path(f"{wrapper_path}.yaghm.backup")


def commands_path(phooks, hook):
    return Path(phooks) / f"{hook}.yaghm.commands"
