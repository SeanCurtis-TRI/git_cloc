#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

# Simple wrapper to the `cloc` script to enable analysis
# of lines of code between git branches in drake.

# For tab complete, you must have argcomplete installed:
#  https://pypi.python.org/pypi/argcomplete

import functools
import re
import subprocess

import numpy as np


def subshell(cmd, suppress_error=False, strip=True):
    try:
        if isinstance(cmd, list):
            output = subprocess.check_output(cmd, encoding="utf8")
        else:
            assert isinstance(cmd, str)
            output = subprocess.check_output(cmd, shell=True, encoding="utf8")
    except subprocess.CalledProcessError as e:
        if suppress_error:
            return None
        else:
            raise e
    if strip:
        return output.strip()
    else:
        return output


class Count:
    '''The counts of modifications'''
    def __init__(self, add=0, mod=0, rem=0):
        self.added = add
        self.modified = mod
        self.removed = rem

    def __int__(self):
        return self.added + self.modified + self.removed


# @functools.total_ordering
class FileCount:
    '''The count for a single file'''
    def __init__(self, file_name):
        '''Ctor.

        @param file_name   The name of the file (a string).
        '''
        self.file_name = file_name
        self.code = Count()
        self.comment = Count()
        self.blank = Count()

    def sorting_key(self):
        return (self.file_name,)

    def __str__(self):
        return f'{self.file_naeme} ({self.code}, {self.comment}, {self.blank})'

    def modified(self, code, comment, blank):
        '''Updates the modify counts with the given values'''
        self.code.modified += code
        self.comment.modified += comment
        self.blank.modified += blank

    def added(self, code, comment, blank):
        '''Updates the modify counts with the given values'''
        self.code.added += code
        self.comment.added += comment
        self.blank.added += blank

    def removed(self, code, comment, blank):
        '''Updates the modify counts with the given values'''
        self.code.removed += code
        self.comment.removed += comment
        self.blank.removed += blank

    def code_count(self):
        return int(self.code)

    def blank_count(self):
        return int(self.blank)

    def comment_count(self):
        return int(self.comment)


def parse_cloc_output(console_output):
    '''Parses the cloc output and produces a list of FileCount objects.'''
    lines = console_output.split('\n')
    # regular expressions to catch lines.
    divider_re = re.compile('^-+$')
    file_header_re = re.compile(r'File\s+blank\s+comment\s+code')
    sum_header_re = re.compile('SUM:')
    count_re = re.compile(r'([a-z]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)')
    START = 0
    FILES = 1
    SUM = 2
    state = START
    files = []
    for line in lines:
        line = line.strip()
        if divider_re.match(line):
            continue
        if state == START:
            if file_header_re.match(line):
                state = FILES
        elif state == FILES:
            m = count_re.match(line)
            if m:
                # udpate counts in current file count
                category = m.group(1)
                blank_count = int(m.group(2))
                comment_count = int(m.group(3))
                code_count = int(m.group(4))
                file = files[-1]
                if category == 'modified':
                    file.modified(code_count, comment_count, blank_count)
                elif category == 'added':
                    file.added(code_count, comment_count, blank_count)
                elif category == 'removed':
                    file.removed(code_count, comment_count, blank_count)
            else:
                if sum_header_re.match(line): break
                else:
                    # create new file count
                    files.append(FileCount(line))
    files.sort(key=FileCount.sorting_key)
    return files

def summary_table(files):
    '''Prints a summary of changes by modification type.
    Difference    added  modified   removed
    ---------------------------------------
    code          x1     x2         x3
    comments      y1     y2         y3
    blank         z1     z2         z3
    '''
    data = np.zeros((3, 3), dtype=np.int)

    def update_category(table, row, count):
        table[row, 0] += count.added
        table[row, 1] += count.modified
        table[row, 2] += count.removed
    for f in files:
        update_category(data, 0, f.code)
        update_category(data, 1, f.comment)
        update_category(data, 2, f.blank)

    row_format = '{0:<20}{1:<7}{2:<10}{3:<9}'
    header = row_format.format('Category', 'added', 'modified', 'removed')
    divider = '-' * len(header)
    print(header)
    print(divider)
    labels = ('code', 'comments', 'blank')
    for i, label in enumerate(labels):
        print(row_format.format(label, data[i, 0], data[i, 1], data[i, 2]))
    totals = np.sum(data, axis=0)
    print(divider)
    print(row_format.format('TOTAL', totals[0], totals[1], totals[2]))

def print_table(files):
    '''Given a list of files, prints out a table'''
    SPACE = 2
    name_width = max( [len(x.file_name) for x in files] ) + SPACE
    code_width = len('Code') + SPACE
    comment_width = len('Comment') + SPACE
    blank_width = len('Blank') + SPACE
    col_format = (f'| {{{{0:{{fill}}<{name_width}}}}}'
                  f'| {{{{1:{{fill}}<{code_width}}}}}'
                  f'| {{{{2:{{fill}}<{comment_width}}}}}'
                  f'| {{{{3:{{fill}}<{blank_width}}}}}|')
    divider = col_format.format(fill='-')
    data_format = col_format.format(fill=' ')

    print(data_format.format('Files', 'Code', 'Comment', 'Blank'))
    print(divider.format('', '', '', ''))
    for f in files:
        print(data_format.format(
                                f.file_name,
                                f.code_count(),
                                f.comment_count(),
                                f.blank_count()))

def friendly_commit(commit, name=None):
    ''' Format as "name (sha)" '''
    sha = subshell('git rev-parse --short {}'.format(commit))
    if name:
        order = (name, sha)
    else:
        order = ("'{}'".format(commit), sha)
    return "{} ({})".format(*order)

def run_cloc(commits):
    '''Runs cloc on the arguments'''
    assert len(commits) <= 2
    src_commit = None
    src_name = None
    if len(commits) == 0:
        src_commit = None
        dst_commit = 'HEAD'
    elif len(commits) == 1:
        src_commit = None
        dst_commit = commits[0]
    else:
        src_commit, dst_commit = commits
    if src_commit is None:
        cmd = f'git merge-base master {dst_commit}'
        src_commit = subshell(cmd)
        src_name = f"$({cmd})"

    src_commit_friendly = friendly_commit(src_commit, src_name)
    dst_commit_friendly = friendly_commit(dst_commit)
    print(
        f"Computing difference between {src_commit_friendly} and "
        f"{dst_commit_friendly}.\n")

    output = subshell([
        'cloc', '--lang-no-ext=Python', '--by-file',
        '--git', '--diff', src_commit,  dst_commit])

    file_counts = parse_cloc_output(output)
    summary_table(file_counts)


def _arg_get_branches(prefix, **kwargs):
    '''List the local branches in the git repository'''
    # @ref https://stackoverflow.com/a/40122019/7829525
    output = subshell("git for-each-ref --format='%(refname:short)' refs/heads",
                      suppress_error=True)
    if output is None:
        argcomplete.warn("Failed to get branches")
        return []
    branches = [b.strip() for b in output.split('\n') if b]
    if prefix:
        branches = filter(lambda x: x.startswith(prefix), branches)
    return branches

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="""
This will produce a table comparing the adds/removes/modifies on the difference
between two commits.

The commits can be any normal git hash descriptor such as: branch names, tag
names, commit values, relative commits, etc.
""".strip())
    parser.add_argument(
        'commit1', type=str, nargs='?',
        help='The base commit to compare against. If no commits are ' +
             'provided, then HEAD will be compared to its merge-base with ' +
             'master.'
        ).completer = _arg_get_branches
    parser.add_argument(
        'commit2', type=str, nargs='?',
        help='The commit to compare against the base commit. ' +
             'If omitted, then commit1 will be compared against ' +
             'its merge-base of master.'
        ).completer = _arg_get_branches

    # Provide argcomplete functionality if it is available.
    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except ImportError:
        pass

    parsed = parser.parse_args()
    # Remove `None` elements.
    commits = [commit for commit in [parsed.commit1, parsed.commit2] if commit]

    run_cloc(commits)
