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

import logging
import functools
import json

from flask import Flask
from flask import request

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.hybrid import hybrid_property


# ###############################################
# Boilerplate and helpers
# ###############################################


# Control * imports.
__all__ = ['app', 'db']

app = Flask(__name__)
db = SQLAlchemy()


def admin_required(func):
    '''
    '''
    
    @functools.wraps(func)
    def wrapper():
        pass
        
    return wrapper
    
    
def asset_detail(asset_type, asset_class, name, cls):
    ''' Creates a detail with the given name and the supplied cls,
    specific to the passed type and class.
    '''
        
    @hybrid_property
    def detail(self):
        ''' Read an existing detail.
        '''
        if self.asset_class != asset_class or self.asset_type != asset_type:
            raise AttributeError(name)
        
        else:
            try:
                return json.loads(self._details)[name]
            
            except KeyError:
                raise AttributeError(name)
        
    @detail.setter
    def detail(self, value):
        ''' Detail modification isn't as thoroughly vetted as asset
        creation. It's immutable in the API, but not in the internal
        model.
        '''
        # Error trap: attempt to assign a detail for a mismatched type/class
        if self.asset_class != asset_class or self.asset_type != asset_type:
            raise AttributeError(name)
        
        # Error trap: detail value doesn't match spec
        elif not isinstance(value, cls):
            raise TypeError(repr(value) + ' is not ' + repr(cls))
        
        # On-the-fly generation of json, so that we have a single source of
        # truth. Alternatively we could modify the sqlalchemy "magic", but this
        # is easier for a demo app / MVP
        if self._details:
            details = json.loads(self._details)
        else:
            details = {}
        
        details[name] = value
        self._details = json.dumps(details)
        
    return detail


# ###############################################
# Lib
# ###############################################


class Asset(db.Model):
    ''' Server-side representation of an asset. This class manages all
    input validation, etc.
    
    Implementation note: we could use @validates for the attributes, but
    instead, we've opted to use @hybrid_property so we can defensively
    enforce immutable name/type/class while we're at it.
    '''
    __tablename__ = 'assets'
    _name = db.Column('name', db.String(64), primary_key=True, nullable=False)
    # These are probably bigger than they need to be, but unless we're planning
    # on having hundreds of millions of assets... might as well have headroom
    _asset_type = db.Column('type', db.String(128), nullable=False)
    _asset_class = db.Column('class', db.String(128), nullable=False)
    # Just store details as a nullable json blob
    _details = db.Column('details', db.Text)
    
    def __init__(self, name, asset_type, asset_class, **details):
        ''' Create an asset.
        '''
        
    @hybrid_property
    def name(self):
        '''
        '''
        
    @name.setter
    def name(self, value):
        '''
        '''
        
    @hybrid_property
    def asset_type(self):
        '''
        '''
        
    @asset_type.setter
    def asset_type(self, value):
        '''
        '''
        
    @hybrid_property
    def asset_class(self):
        '''
        '''
        
    @asset_class.setter
    def asset_class(self, value):
        '''
        '''
    
    # This makes it extremely easy to add details; see implementation note in
    # README about the implied context behind asset details
    gain = asset_detail('antenna', 'yagi', 'gain', float)
    diameter = asset_detail('antenna', 'dish', 'diameter', float)
    radome = asset_detail('antenna', 'dish', 'radome', bool)


@app.route('/assets/v1/', methods=['POST'])
def make_new_asset():
    '''
    '''


@app.route('/assets/v1/', methods=['GET'])
def show_all_assets():
    '''
    '''


@app.route('/assets/v1/<name>', methods=['GET'])
def show_single_asset(name):
    '''
    '''
    
    
@app.route('/assets/v1/sat')
def filter_sats():
    '''
    '''
    
    
@app.route('/assets/v1/sat/dove')
def filter_dove():
    '''
    '''
    
    
@app.route('/assets/v1/sat/rapideye')
def filter_rapideye():
    '''
    '''
    
    
@app.route('/assets/v1/ant/')
def filter_ants():
    '''
    '''
    
    
@app.route('/assets/v1/ant/dish')
def filter_dish():
    '''
    '''
    
    
@app.route('/assets/v1/ant/yagi')
def filter_yagi():
    '''
    '''
