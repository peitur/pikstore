 #!/usr/bin/env python3

import os, sys, re
import base64

import piks.utils
import piks.defaults
import piks.validate
import piks.runner

from Crypto.PublicKey import RSA

from pprint import pprint

class CryptRSA( object ):

    def __init__( self, **opt ):
        self._debug = False

        self._pem = "\n".join( opt['pem'] )
        self._password = opt['password']

        pprint( self._pem )
        print( "PASSWORD: %s" % ( self._password ) )

        self._key = RSA.importKey( self._pem,  passphrase=self._password )


    def get_key( self ):
        return self._key

    def encrypt( self, **opt ):
        pass

    def decrypt( self, **opt ):
        pass


if __name__ == "__main__":
    passwd = piks.file.file_hash( os.path.realpath( __file__ ) )
    print("PASSWORD: %s"%( passwd ))

    pem = list()
    privkey = piks.runner.CreatePrivateKey( password=passwd, bits="512", encode="aes256").run()
    pubkey = piks.runner.CreatePublicKey( password=passwd, privatekey=privkey, encode="aes256" ).run()

    rsa = CryptRSA( pem=privkey, password=passwd )
    pprint( rsa.get_key() )
