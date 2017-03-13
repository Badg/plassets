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

import unittest
import flask_testing
import tempfile
import os
import plassets

from plassets import Asset


# ###############################################
# Test vectors
# ###############################################


dove1 = (
    Asset('dove1', 'satellite', 'dove'),
    {
        'name': 'dove1',
        'type': 'satellite',
        'class': 'dove'
    }
)
dove2 = (
    Asset('dove2', 'satellite', 'dove'),
    {
        'name': 'dove2',
        'type': 'satellite',
        'class': 'dove'
    }
)
rapideye1 = (
    Asset('rapideye1', 'satellite', 'rapideye'),
    {
        'name': 'rapideye1',
        'type': 'satellite',
        'class': 'rapideye'
    }
)
rapideye2 = (
    Asset('rapideye2', 'satellite', 'rapideye'),
    {
        'name': 'rapideye2',
        'type': 'satellite',
        'class': 'rapideye'
    }
)
dish1 = (
    Asset('dish1', 'antenna', 'dish'),
    {
        'name': 'dish1',
        'type': 'antenna',
        'class': 'dish'
    }
)
dish2 = (
    Asset('dish2', 'antenna', 'dish'),
    {
        'name': 'dish2',
        'type': 'antenna',
        'class': 'dish'
    }
)
yagi1 = (
    Asset('yagi1', 'antenna', 'yagi'),
    {
        'name': 'yagi1',
        'type': 'antenna',
        'class': 'yagi'
    }
)
yagi2 = (
    Asset('yagi2', 'antenna', 'yagi'),
    {
        'name': 'yagi2',
        'type': 'antenna',
        'class': 'yagi'
    }
)


# ###############################################
# Testing
# ###############################################


# This is a super-quick test setup due to time constraints. It's not expected
# to be exhaustive, but the most important / highest-impact code routes are
# tested
class AppTester(flask_testing.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.db_fd, cls.db_path = tempfile.mkstemp()
        
    @classmethod
    def tearDownClass(cls):
        # Close the database and clean it up manually
        os.close(cls.db_fd)
        os.unlink(cls.db_path)
    
    def setUp(self):
        self.client = plassets.app.test_client()
        plassets.db.create_all()
        
    def tearDown(self):
        plassets.db.session.remove()
        plassets.db.drop_all()
        
    def create_app(self):
        return plassets.create_app(
            TESTING = True,
            SQLALCHEMY_DATABASE_URI = 'sqlite:///' + self.db_path,
            SQLALCHEMY_TRACK_MODIFICATIONS = False
        )
        
    def test_new_asset(self):
        '''
        '''
        
    def test_get_single(self):
        '''
        '''
        
    def test_get_all(self):
        '''
        '''
        
    def test_filter_sat(self):
        '''
        '''
        
    def test_filter_dove(self):
        '''
        '''
        
    def test_filter_rapideye(self):
        '''
        '''
        
    def test_filter_ants(self):
        '''
        '''
        
    def test_filter_dish(self):
        '''
        '''
        
    def test_filter_yagi(self):
        '''
        '''
        
        
class AssetTester(unittest.TestCase):
    ''' Ancillary testing for plassets assets to ensure they correctly
    deal with input.
    '''
    
    def test_dove(self):
        '''
        '''
        
    def test_rapideye(self):
        '''
        '''
        
    def test_dish(self):
        '''
        '''
        
    def test_yagi(self):
        '''
        '''


if __name__ == '__main__':
    unittest.main()