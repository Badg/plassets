'''
LICENSING
-------------------------------------------------

Plassets: Planet Labs asset store coding exercise

    The MIT license (MIT)

    Copyright 2017 Nick Badger.

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation files
    (the "Software"), to deal in the Software without restriction,
    including without limitation the rights to use, copy, modify, merge,
    publish, distribute, sublicense, and/or sell copies of the Software,
    and to permit persons to whom the Software is furnished to do so,
    subject to the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
    BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
    ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
    CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

------------------------------------------------------
'''

import os
import tempfile
import argparse

from . import create_app
from . import db


root_parser = argparse.ArgumentParser()
root_parser.add_argument(
    '--host', '-H',
    action = 'store',
    type = str,
    default = '127.0.0.1',
    help = 'What host to serve from. Defaults to localhost.'
)
root_parser.add_argument(
    '--port', '-p',
    action = 'store',
    type = int,
    default = 8080,
    help = 'What port to serve from. Defaults to 8080.'
)
        

if __name__ == '__main__':
    args = root_parser.parse_args()
    
    try:
        db_fd, db_path = tempfile.mkstemp()
        app = create_app(
            TESTING = False,
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db_path,
            SQLALCHEMY_TRACK_MODIFICATIONS = False
        )
        db.create_all()
        app.run(host=args.host, port=args.port)
        
    finally:
        os.close(db_fd)
        os.unlink(db_path)
