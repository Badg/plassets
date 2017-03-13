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
import re

from flask import Flask
from flask import request

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.hybrid import hybrid_property


# ###############################################
# Boilerplate and helpers
# ###############################################


# Control * imports.
__all__ = ['app', 'db']


# Flask stuff
app = Flask(__name__)
db = SQLAlchemy()


# Decorators
def admin_required(func):
    '''
    '''
    
    @functools.wraps(func)
    def wrapper():
        pass
        
    return wrapper
    

# Misc helpers
NAME_PATTERN = re.compile(r'^[A-z0-9][A-z0-9\_\-]{3,63}$')


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
    _name = db.Column('name', db.String(64), primary_key=True, nullable=False,
                      unique=True, index=True)
    # These are probably bigger than they need to be, but unless we're planning
    # on having hundreds of millions of assets... might as well have headroom
    _asset_type = db.Column('type', db.String(128), nullable=False, index=True)
    _asset_class = db.Column('class', db.String(128), nullable=False,
                             index=True)
    # Just store details as a nullable json blob
    _details = db.Column('details', db.Text)
    
    VALID_TYPES = {'antenna', 'satellite'}
    VALID_CLASSES = {
        'satellite': {'dove', 'rapideye'},
        'antenna': {'dish', 'yagi'}
    }
    
    def __init__(self, name, asset_type, asset_class, **details):
        ''' Create an asset.
        '''
        # If the order of these being declared changes, we will need to add
        # immutability checks to asset types and classes
        self.name = name
        self.asset_type = asset_type
        self.asset_class = asset_class
        
        # Quick and dirty enforcing that **details are, in fact, details
        if any(key not in dir(Asset) for key in details):
            raise AttributeError()
        
        for key, value in details.items():
            setattr(self, key, value)
        
    @hybrid_property
    def name(self):
        ''' Get the name.
        '''
        return self._name
        
    @name.setter
    def name(self, value):
        ''' Set the name, checking it for validity on the way. Also,
        ensure immutability, both locally (for this instance) and in the
        database.
        '''
        if self._name:
            raise AttributeError('Cannot mutate names.')
        
        # If we got here, the name is not yet defined. Error trap first.
        if not re.match(NAME_PATTERN, value):
            raise ValueError(value)
        
        # Ensure uniqueness (there's a small race condition here, but I'm
        # assuming asset creation will be slow enough for it to be ignored)
        q = db.session.query(Asset).filter(Asset._name == value)
        if db.session.query(q.exists()).scalar():
            raise ValueError(value)
            
        self._name = value
        
    @hybrid_property
    def asset_type(self):
        ''' Get the asset type.
        '''
        return self._asset_type
        
    @asset_type.setter
    def asset_type(self, value):
        ''' Set the asset type, checking it for validity. Also ensure
        immutability of both instance (database immutability is handled
        through the name check).
        '''
        if self._asset_type:
            raise AttributeError('Cannot mutate asset type.')
        
        # If we got here, the type is not yet defined. Error trap first.
        if value not in self.VALID_TYPES:
            raise ValueError(value)
            
        self._asset_type = value
        
    @hybrid_property
    def asset_class(self):
        ''' Get the asset class.
        '''
        return self._asset_class
        
    @asset_class.setter
    def asset_class(self, value):
        ''' Set the asset class, checking it for validity. Also ensure
        immutability of both instance (database immutability is handled
        through the name check).
        '''
        if self._asset_class:
            raise AttributeError('Cannot mutate asset class.')
        
        # If we got here, the name is not yet defined. Error trap first.
        # This relies upon the order of setting, as defined in __init__.
        if value not in self.VALID_CLASSES[self.asset_type]:
            raise ValueError(value)
            
        self._asset_class = value
    
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
