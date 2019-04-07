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


class CreatePrivateKey( GenericCommand ):

    def __init__( self, **opt ):
        self._debug = False
        self._password = opt['password']
        self._algorithm = opt['algorithm']
        self._bits = "4096"
        self._encode = "des3"

        if 'debug' in opt and opt['debug'] in (True,False):
            self._debug = opt['debug']

        if 'encode' in opt and opt['encode'] in ("des3","aes128","aes192", "aes256","camellia128","camellia192","camellia256"):
            self._encode = opt['encode']

        command = [ "genrsa",
            "-%s" % ( self._encode ),
            "-passout", self._password,
            self._bits
        ]

        GenericCommand.__init__( self, command, debug=self._debug )


    def run( self ):
        pass

    def get_privatekey( self ):
        return self._pkey


class CreatePublicKey( GenericCommand ):

    def __init__( self, **opt ):
        GenericCommand.__init__( self, None, **opt  )
        self._password = opt['password']
        self._algorith = opt['algorith']
        self._pkey = opt['privatekey']

    def run( self ):
        pass


if __name__ == "__main__":
    pprint( CreatePrivateKey( "test" ).run() )
