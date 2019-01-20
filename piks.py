#!/usr/bin/env python3

import os, re, sys
import getopt, traceback
from pprint import pprint

## ugly solution for something that should not be like this... libs should be put into standard site libs
sys.path.append( "%s/../" % ( os.path.dirname( os.path.realpath( __file__ ) )) )

import piks.command
import piks.defaults

def usage():
    pass

if __name__ == "__main__":
    options = dict()

    options['debug'] = False
    options['output'] = "%s/%s" % ( piks.defaults.PIKS_DEFAULT_DIR, piks.defaults.PIKS_DEFAULT_FILE )
    options['source'] = None


    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:s:", ["help", "output=", "debug", "source="])
    except getopt.GetoptError as err:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-o","--output"):
            options['output'] = a
        if o in ("-s","--source"):
            options['source'] = a
        elif o in ("--debug"):
            options['debug'] = True
        else:
            usage()
            sys.exit(1)

    try:
        kcmp.compiler.Compiler( options ).run()
    except Exception as e:
        if options['debug']: print("\n*** Message:")
        print( "ERROR: Compiler failed: %s" % (e) )
        if options['debug']:
            # https://docs.python.org/3/library/traceback.html
            print("\n*** Traceback:")
            exc_type, exc_value, exc_traceback = sys.exc_info()

            print("\n*** print_tb:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

            print("\n*** print_exception:")
            # exc_type below is ignored on 3.5 and later
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)

            print("\n*** print_exc:")
            traceback.print_exc(limit=2, file=sys.stdout)

            print("\n*** format_exc, first and last line:")
            formatted_lines = traceback.format_exc().splitlines()
            print(formatted_lines[0])
            print(formatted_lines[-1])

            print("\n*** format_exception:")
            # exc_type below is ignored on 3.5 and later
            print(repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

            print("\n*** extract_tb:")
            print(repr(traceback.extract_tb(exc_traceback)))

            print("\n*** format_tb:")
            print(repr(traceback.format_tb(exc_traceback)))

            print("\n*** tb_lineno:", exc_traceback.tb_lineno)
        sys.exit(4)
