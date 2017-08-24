#!/usr/bin/env python

# Simple wrapper to the `cloc` script to enable analysis
# of lines of code between git branches in drake.

from optparse import OptionParser
import re
import subprocess

class Count:
    '''The counts of modifications'''
    def __init__(self, add=0, mod=0, rem=0):
        self.added = add
        self.modified = mod
        self.removed = rem

    def __int__(self):
        return self.added + self.modified + self.removed

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

    def __cmp__(self, other):
        return cmp(self.file_name, other.file_name)

    def __str__(self):
        return '%s (%d, %d, %d)' % (self.file_name,
                                    self.code,
                                    self.comment,
                                    self.blank)
                                     
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
    file_header_re = re.compile('File\s+blank\s+comment\s+code')
    sum_header_re = re.compile('SUM:')
    count_re = re.compile('([a-z]+)\s+([0-9]+)\s+([0-9]+)\s+([0-9]+)')
    START = 0
    FILES = 1
    SUM = 2
    state = START
    files = []
    for line in lines:
        line = line.strip()
        if (divider_re.match(line)): continue

        if (state == START):
            if (file_header_re.match(line)):
                state = FILES
        elif (state == FILES):
            m = count_re.match(line)
            if m:
                # udpate counts in current file count
                category = m.group(1)
                blank_count = int(m.group(2))
                comment_count = int(m.group(3))
                code_count = int(m.group(4))
                file = files[-1]
                if (category == 'modified'):
                    file.modified(code_count, comment_count, blank_count)
                elif (category == 'added'):
                    file.added(code_count, comment_count, blank_count)
                elif (category == 'removed'):
                    file.removed(code_count, comment_count, blank_count)
            else:
                if (sum_header_re.match(line)): break
                else:
                    # create new file count
                    files.append(FileCount(line))
    files.sort()
    return files

def print_table(files):
    '''Given a list of files, prints out a table'''
    SPACE = 2
    name_width = max( [len(x.file_name) for x in files] ) + SPACE
    code_width = len('Code') + SPACE
    comment_width = len('Comment') + SPACE
    blank_width = len('Blank') + SPACE
    col_format = ('| {{{{0:{{fill}}<{name_w}}}}}'
                  '| {{{{1:{{fill}}<{code_w}}}}}'
                  '| {{{{2:{{fill}}<{comment_w}}}}}'
                  '| {{{{3:{{fill}}<{blank_w}}}}}|').format(
                      name_w=name_width,
                      code_w=code_width,
                      comment_w=comment_width,
                      blank_w=blank_width)
    divider = col_format.format(fill='-')
    data_format = col_format.format(fill=' ')

    print data_format.format('Files', 'Code', 'Comment', 'Blank')
    print divider.format('', '', '', '')
    for f in files:
        print data_format.format(
                                f.file_name,
                                f.code_count(),
                                f.comment_count(),
                                f.blank_count())
    
def run_cloc(args):
    '''Runs cloc on the arguments'''
    if (len(args) < 1):
        print "No git commits provided"
        return False
    elif (len(args) > 2):
        print "Too many arguments provided"
        return False
    elif (len(args) < 2):
        src_hash = 'master'
        dst_hash = args[0]
    else:
        src_hash, dst_hash = args

    print "Computing difference between '%s' and '%s'." % (src_hash, dst_hash)

    try:
        output = subprocess.check_output(['cloc', 
                                          '--lang-no-ext=Python', 
                                          '--by-file',
                                          '--git', 
                                          '--diff', 
                                          src_hash, 
                                          dst_hash])
    except subprocess.CalledProcessError as e:
        print e
        return False

    file_counts = parse_cloc_output(output)
    print_table(file_counts)
    return True

def main():
    parser = OptionParser()

    options, args = parser.parse_args()

    if not run_cloc(args):
        print
        parser.print_help()

if __name__ == '__main__':
    main()
