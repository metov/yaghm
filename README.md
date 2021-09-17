# Yet Another Git Hook Manager
Yaghm is a minimal [git hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) manager. You write a simple YAML config file listing the hooks you want. `yaghm enable` enables them in your repo. `yaghm disable` disables them.:

* Yaghm is simple. Hooks are not rocket science. The config is just a list of shell commands. When you enable them, yaghm writes a wrapper script in `.git/hooks` that calls the commands you gave. If they work in your shell they'll work in the hook.
* Because it's so simple, the documentation is complete, troubleshooting is easy and writing your own extensions is a breeze.
* **Your** workflow, not mine. You can store the config wherever you want. Maybe you version your hooks, maybe you don't, maybe you keep them in a separate repo, or your home dir, or your dotfiles...

## Usage
To use yaghm, you create a config that lists your hook commands (see [detailed syntax](doc/config.md)):

```yaml
pre-commit:
  - ...
  # Assuming you have a program called current_branch_not
  - current_branch_not master 
  - enable: black --check .
    install: pip install black
    update: pip install -U black
  - enable: require_version_bump master setup.py
    update: pip install -U metovhooks

post-commit:
  - ...
```

You can use `yaghm -h` to see general help. There are three main subcommands (which also support `-h`): 

* Enable hooks: `yaghm enable`
* List enabled hooks: `yaghm list`
* Disable hooks: `yaghm disable`

When using `enable` and `disable`, if you pass `--dryrun` no files will actually be written.

You can also run custom hook commands (e.g. update) with `yaghm update`. If any hooks in your config [specify the command](doc/config.md), it will be executed.

## Install
Install with `pip install yaghm`

## Further reading

* [How it works](doc/technical.md)
* [Config syntax](doc/config.md)
* [Developing hooks](doc/custom-hooks.md)
