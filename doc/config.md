# Configuration syntax
A yaghm config is a YAML dictionary where keys are names of git hooks (eg. `pre-commit`, `post-commit`, etc.) and each value is a YAML list. Every item in the list corresponds to a hook. Items are either strings or dictionaries. 

* Strings are treated as shell commands that will be executed by the hook.
* Dictionaries must have an `enable` key which is where you provide the hook command. They can also have additional key-values where the key is the name of the command (eg. `install`) and the value is the corresponding command.

By specifying an `install` or `update` command for several hooks, for example, you can easily install or update all your hooks by running `yaghm install` or `yaghm update`.

You can also check out the [`yaghm.yml`](../yaghm.yml) file in this repository. Since I use yaghm to manage my hooks for this repo, this doubles as a real-world example.
