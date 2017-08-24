#!/usr/bin/env python

# Simple wrapper to the `cloc` script to enable analysis
# of lines of code between git branches in drake.

from optparse import OptionParser
import subprocess

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

    subprocess.call(['cloc', 
                     '--lang-no-ext=Python', 
                     '--git', 
                     '--diff', 
                     src_hash, 
                     dst_hash])
    return True

def main():
    parser = OptionParser()

    options, args = parser.parse_args()

    if not run_cloc(args):
        print
        parser.print_help()

if __name__ == '__main__':
    main()
