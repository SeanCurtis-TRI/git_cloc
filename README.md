This provides source lines of code documentation between git commits.

USAGE
=====

`git_cloc branch1 branch2`

This will produce a table comparing the adds/removes/modifies on the difference
between `branch1` and `branch2`.

The arguments `branch1` and `branch2` can be any normal git hash descriptor
such as: branch names, tag names, commit values, relative commits, etc.

Providing only a single branch will compare it with master:

`git_cloc branch1`

INSTALLATION
============

In some bin directory in your path:

`ln -s $PATH_TO_GIT_CLOC/drake_cloc.py git_cloc`

Place the tab completion file in the following location:
`sudo cp git_cloc.sh /etc/bash_completion.d/.`

If it isn't getting sourced in new terminals create the file:
`~/.bash_completion`

and add the following line:

`. /etc/bash_completion.d/git_cloc.sh`


Prerequisites
-------------

- This uses Python 2.7.
- It uses the module `argcomplete`. To install:
  `pip install argcomplete`
- It makes use of the cloc project which can be cloned from here:
   https://github.com/AlDanial/cloc


