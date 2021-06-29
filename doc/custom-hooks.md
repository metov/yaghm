# Developing hooks
Yaghm treats hooks as simple shell commands, so "developing" hooks is very easy: Make sure you can run the command in your shell, and then paste it into yaghm's config.

This works best if your command calls only single, self-contained scripts and programs installed on your system. However, occasionally you may need something a little bit more complex, such as a script that reads from a data file in the same directory as itself or imports another script. In these situations the best thing to do is to turn your scripts into packages, install them on your system, and now the hook once again becomes a simple case of calling installed programs.

If you can't make a package or simply don't want to, it's not the end of the world. You just have to be mindful that when git executes hooks, the working directory is the repo root. So if `/some/script/used/as/hook.py` needs to read `/some/script/used/as/data.txt` at runtime, it cannot just do `load("./data.txt")` as that will now point to (probably non-existent) `/my/git/repo/data.txt`. There are two obvious solutions to this:
 
1. Specify absolute paths. This of course means you have to be careful when moving you hook script around. 
2. Obtain the script's own location at runtime and go from there. On Python you can do this using `__file__`. The main caveat is, watch out when there's a lot of symlink/bind-mount trickery happening.

If you want to make yaghm install your hook program when you enable the hook, you can use the custom commands. For example you can add `install: pip install black`, and your hooks set up might be something like `yaghm install && yaghm enable`. 
