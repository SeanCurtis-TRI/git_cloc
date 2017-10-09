This provides source lines of code documentation between git commits.

USAGE
=====

```
usage: git_cloc [-h] [commit1] [commit2]

This will produce a table comparing the adds/removes/modifies on the
difference between two commits. The commits can be any normal git hash
descriptor such as: branch names, tag names, commit values, relative commits,
etc.

positional arguments:
  commit1     The base commit to compare against. If no commits are provided,
              then HEAD will be compared to its merge-base with master.
  commit2     The commit to compare against the base commit. If omitted, then
              commit1 will be compared against master.

optional arguments:
  -h, --help  show this help message and exit
```

INSTALLATION
============

Instructions
------------

In some bin directory in your `$PATH`:

`ln -s $PATH_TO_GIT_CLOC/drake_cloc.py git_cloc`

Either in `/etc/bash_completion.d/*.sh`, `~/.bashrc`, or `~/.bash_aliases`, ensure that your shell will autocomplete your binary:

    eval "$(register-python-argcomplete git_cloc)"

*NOTE*: Global autocompletion from `argcomplete` may work, but has not been tested.

Prerequisites
-------------

- This uses Python 2.7 with the following modules:
    - `numpy`
    - `argcomplete`
    - Options to install:
      - `pip install MODULE_NAME`
      - `sudo apt install python-MODULE_NAME`
- It makes use of the `cloc` project which can be cloned from [https://github.com/AlDanial/cloc](https://github.com/AlDanial/cloc)
    - This must contain at least commit `cbd39bc`.
    - It assumes that the `cloc` command is visible in the execution path.
