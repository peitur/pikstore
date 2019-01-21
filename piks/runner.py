#!/usr/bin/env python3

import os, sys, re
import subprocess, shlex

import piks
import piks.utils
import piks.validate
import piks.file

from pprint import pprint


class GenericCommand( object ):

    def __init__(self, cmd, **opt ):
        self._cmd = cmd
        self._debug = False
        self._command = "openssl"
        self._stdin = None

        if piks.KEY_SYSTEM_DEBUG in opt and opt[ piks.KEY_SYSTEM_DEBUG ] in (True,False):
            self._debug = opt[ piks.KEY_SYSTEM_DEBUG ]

        if piks.KEY_SYSTEM_COMMAND in opt and opt[ piks.KEY_SYSTEM_COMMAND ] in ("openssl"):
            self._command = opt[ piks.KEY_SYSTEM_COMMAND ]

        if piks.KEY_SYSTEM_STDIN in opt:
            self._stdin = opt[ piks.KEY_SYSTEM_STDIN ]


    def run( self, **opt ):
        result = list()
        cmd = self._cmd
        stdin = None

        if type( cmd ).__name__ == "str":
            cmd = shlex.split( cmd )

        cmd = [ self._command ] + cmd

        if self._debug: print( " ".join( cmd ) )

        if self._stdin:
            stdin=subprocess.PIPE

        prc = subprocess.Popen( cmd, universal_newlines=True, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        if stdin:
            for line in self._stdin:
                prc.stdin.write( "%s\n" % (line) )
            prc.stdin.close()

        for line in prc.stdout.readlines():
            result.append( line.lstrip().rstrip() )

#        if prc.returncode != 0:
#            for line in prc.stderr.readlines():
#                print( "ERROR: %s" %(line.lstrip().rstrip()))

        return result


class CreatePrivateKey( GenericCommand ):

    def __init__( self, **opt ):

        self._valuemap = {
            "debug":{"match":["True","False"]},
            "password":{ "mandatory": True, "match":["^[0-9a-zA-Z_\.]+$"] },
            "algorithm":{ "match":["rsa","dsa"] },
            "bits":{ "match":["^[0-9]+$"] },
            "encode":{ "match":["des3","aes128","aes192", "aes256","camellia128","camellia192","camellia256"] }
        }

        piks.validate.Validator( self._valuemap, strict=False, debug=True ).validate( opt )

        self._debug = False
        self._password = opt['password']
        self._algorithm = "rsa"
        self._bits = "4096"
        self._encode = "des3"

        if 'debug' in opt and opt['debug'] in (True,False): self._debug = opt['debug']
        if 'encode' in opt: self._encode = opt['encode']
        if 'algorithm' in opt: self._algorithm = opt['algorithm']
        if 'bits' in opt: self._bits = opt['bits']

        command = [ "gen%s" % ( self._algorithm ),
            "-%s" % ( self._encode ),
            "-passout", "pass:%s" %(self._password),
            self._bits
        ]

        super().__init__( command, debug=self._debug )


    def run( self ):
        self._pkey = super().run()
        return self._pkey

    def get_privatekey( self ):
        return self._pkey


class CreatePublicKey( GenericCommand ):

    def __init__( self, **opt ):
        self._valuemap = {
            "debug":{"match":["True","False"]},
            "algorithm":{ "match":["rsa","dsa"] },
            "password":{ "mandatory": True, "match":["^[0-9a-zA-Z_\.]+$"] },
            "encode": { "mandatory":True, "match":["des3","aes128","aes192", "aes256","camellia128","camellia192","camellia256"]},
            "privatekey":{  "mandatory": True }
        }

        piks.validate.Validator( self._valuemap, strict=False, debug=True ).validate( opt )

        self._debug = False
        self._algorithm = "rsa"
        self._password = opt['password']
        self._encode = opt['encode']
        self._pkey = opt['privatekey']

        if 'debug' in opt and opt['debug'] in (True,False): self._debug = opt['debug']
        if 'algorithm' in opt: self._algorithm = opt['algorithm']

        command = [ self._algorithm,
            "-%s" % ( self._encode ),
            "-passin", "pass:%s" %(self._password),
            "-inform","PEM",
            "-pubout"
        ]

        super().__init__( command, stdin=self._pkey, debug=self._debug )


    def run( self ):
        self._pubkey = super().run()
        return self._pubkey

    def get_publickey( self ):
        return self._pubkey

if __name__ == "__main__":
    passwd = piks.file.file_hash( os.path.realpath( __file__ ) )
    print("PASSWORD: %s"%( passwd ))
    
    privk = CreatePrivateKey( password=passwd, bits="512" ).run()
    pprint( privk )

    pubk = CreatePublicKey( password=passwd, privatekey=privk, encode="des3").run()
    pprint( pubk )
