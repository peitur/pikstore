#!/usr/bin/env python3

import os, sys, re
import subprocess, shlex

import piks
import piks.utils
import piks.validate

from pprint import pprint


class GenericCommand( object ):

    def __init__(self, cmd, **opt ):
        self._cmd = cmd
        self._debug = False
        self._command = "openssl"


        if piks.KEY_SYSTEM_DEBUG in opt and opt[ piks.KEY_SYSTEM_DEBUG ] in (True,False):
            self._debug = opt[ piks.KEY_SYSTEM_DEBUG ]

        if piks.KEY_SYSTEM_COMMAND in opt and opt[ piks.KEY_SYSTEM_COMMAND ] in ("openssl"):
            self._command = opt[ piks.KEY_SYSTEM_COMMAND ]


    def run( self, **opt ):
        result = list()
        cmd = self._cmd


        if type( cmd ).__name__ == "str":
            cmd = shlex.split( cmd )

        cmd = [ self._command ] + cmd

        if self._debug: print( " ".join( cmd ) )

        prc = subprocess.Popen( cmd, universal_newlines=True, stdout=subprocess.PIPE )
        for line in prc.stdout.readlines():
            result.append( line.lstrip().rstrip() )
        return result
