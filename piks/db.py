 #!/usr/bin/env python3

import os, sys, re
import json
import sqlite3

import piks
import piks.utils
import piks.defaults
import piks.validate

from pprint import pprint

DATABASE_KEYS={
    "name":"text primary key",
    "private":"blob not null"
}

class Database( object ):

    def __init__( self, filename, **opt ):
        self._filename = filename

        self._db = sqlite3.connect( self._filename )

    def _commit( self ):
        self._db.commit()

    def _init_db( self ):
        pass

    def insert( self, kvmap ):
        pass

    def query( self, keys, from, where=None, sort=None ):
        pass

if __name__ == "__main__":
    pass
