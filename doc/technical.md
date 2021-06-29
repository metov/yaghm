# How it works
Yaghm puts a simple wrapper script at the hook entrypoint (eg. `.git/hooks/pre-commit`) and a list of commands with matching name 

Yaghm operates based on a config file, which is treated as a wishlist of what hooks *should* be enabled in the target repo. These are composed into a list of commands (eg. `.git/hooks/pre-commit.yaghm.commands`). The actual hook entrypoint (eg. `.git/hooks/pre-commit`) is a simple shell script that calls each command in the list. This shell script will be triggered by git as per the normal hooks behavior.
