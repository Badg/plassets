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
import json
import plassets

from plassets import Asset


# ###############################################
# Test vectors
# ###############################################


def make_vectors():
    dove1 = (
        Asset('dove1', 'satellite', 'dove'),
        {
            u'name': u'dove1',
            u'type': u'satellite',
            u'class': u'dove',
            u'details': {}
        }
    )
    dove2 = (
        Asset('dove2', 'satellite', 'dove'),
        {
            u'name': u'dove2',
            u'type': u'satellite',
            u'class': u'dove',
            u'details': {}
        }
    )
    rapideye1 = (
        Asset('rapideye1', 'satellite', 'rapideye'),
        {
            u'name': u'rapideye1',
            u'type': u'satellite',
            u'class': u'rapideye',
            u'details': {}
        }
    )
    rapideye2 = (
        Asset('rapideye2', 'satellite', 'rapideye'),
        {
            u'name': u'rapideye2',
            u'type': u'satellite',
            u'class': u'rapideye',
            u'details': {}
        }
    )
    dish1 = (
        Asset('dish1', 'antenna', 'dish'),
        {
            u'name': u'dish1',
            u'type': u'antenna',
            u'class': u'dish',
            u'details': {}
        }
    )
    dish2 = (
        Asset('dish2', 'antenna', 'dish'),
        {
            u'name': u'dish2',
            u'type': u'antenna',
            u'class': u'dish',
            u'details': {}
        }
    )
    yagi1 = (
        Asset('yagi1', 'antenna', 'yagi'),
        {
            u'name': u'yagi1',
            u'type': u'antenna',
            u'class': u'yagi',
            u'details': {}
        }
    )
    yagi2 = (
        Asset('yagi2', 'antenna', 'yagi'),
        {
            u'name': u'yagi2',
            u'type': u'antenna',
            u'class': u'yagi',
            u'details': {}
        }
    )
    
    return dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2


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
        ''' Create a new asset. Required to have the x-user header set
        to admin.
        '''
        vecs = make_vectors()
        dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2 = vecs
        
        # Make sure all kinds of assets post successfully
        res = self.client.post('/assets/v1/', data=json.dumps(dove1[1]),
                               headers={'X-User': 'admin'})
        self.assertEqual(200, res.status_code)
        self.assertIsNotNone(Asset.query.get(dove1[1]['name']))
        
        res = self.client.post('/assets/v1/', data=json.dumps(dove2[1]),
                               headers={'X-User': 'admin'})
        self.assertEqual(200, res.status_code)
        self.assertIsNotNone(Asset.query.get(dove2[1]['name']))
        
        res = self.client.post('/assets/v1/', data=json.dumps(rapideye1[1]),
                               headers={'X-User': 'admin'})
        self.assertEqual(200, res.status_code)
        self.assertIsNotNone(Asset.query.get(rapideye1[1]['name']))
        
        res = self.client.post('/assets/v1/', data=json.dumps(rapideye2[1]),
                               headers={'X-User': 'admin'})
        self.assertEqual(200, res.status_code)
        self.assertIsNotNone(Asset.query.get(rapideye2[1]['name']))
        
        res = self.client.post('/assets/v1/', data=json.dumps(dish1[1]),
                               headers={'X-User': 'admin'})
        self.assertEqual(200, res.status_code)
        self.assertIsNotNone(Asset.query.get(dish1[1]['name']))
        
        res = self.client.post('/assets/v1/', data=json.dumps(dish2[1]),
                               headers={'X-User': 'admin'})
        self.assertEqual(200, res.status_code)
        self.assertIsNotNone(Asset.query.get(dish2[1]['name']))
        
        res = self.client.post('/assets/v1/', data=json.dumps(yagi1[1]),
                               headers={'X-User': 'admin'})
        self.assertEqual(200, res.status_code)
        self.assertIsNotNone(Asset.query.get(yagi1[1]['name']))
        
        # And, of course, check "authentication"
        res = self.client.post('/assets/v1/', data=json.dumps(yagi2[1]))
        self.assertEqual(401, res.status_code)
        self.assertIsNone(Asset.query.get(yagi2[1]['name']))
        
    def test_get_single(self):
        ''' Test retrieving a single asset.
        '''
        vecs = make_vectors()
        dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2 = vecs
        plassets.db.session.add(dove1[0])
        plassets.db.session.add(rapideye1[0])
        plassets.db.session.add(dish1[0])
        plassets.db.session.add(yagi1[0])
        plassets.db.session.commit()
        
        # Make sure we get a real response from existant assets.
        res = self.client.get('/assets/v1/' + dove1[1]['name'])
        self.assertEqual(res.json, dove1[1])
        res = self.client.get('/assets/v1/' + rapideye1[1]['name'])
        self.assertEqual(res.json, rapideye1[1])
        res = self.client.get('/assets/v1/' + dish1[1]['name'])
        self.assertEqual(res.json, dish1[1])
        res = self.client.get('/assets/v1/' + yagi1[1]['name'])
        self.assertEqual(res.json, yagi1[1])
        
        # And make sure we get 404s on other assets.
        res = self.client.get('/assets/v1/' + dove2[1]['name'])
        self.assertEqual(res.status_code, 404)
        res = self.client.get('/assets/v1/' + rapideye2[1]['name'])
        self.assertEqual(res.status_code, 404)
        res = self.client.get('/assets/v1/' + dish2[1]['name'])
        self.assertEqual(res.status_code, 404)
        res = self.client.get('/assets/v1/' + yagi2[1]['name'])
        self.assertEqual(res.status_code, 404)
        
    def test_get_all(self):
        ''' Test retrieving all assets.
        '''
        vecs = make_vectors()
        dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2 = vecs
        plassets.db.session.add(dove1[0])
        plassets.db.session.add(rapideye1[0])
        plassets.db.session.add(dish1[0])
        plassets.db.session.add(yagi1[0])
        plassets.db.session.commit()
        
        res = self.client.get('/assets/v1/')
        self.assertEqual(res.json,
                         [dish1[1], dove1[1], rapideye1[1], yagi1[1]])
        
    def test_filter_sat(self):
        ''' Test retrieving only satellites.
        '''
        vecs = make_vectors()
        dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2 = vecs
        plassets.db.session.add(dove1[0])
        plassets.db.session.add(dove2[0])
        plassets.db.session.add(rapideye1[0])
        plassets.db.session.add(rapideye2[0])
        plassets.db.session.add(dish1[0])
        plassets.db.session.add(dish2[0])
        plassets.db.session.add(yagi1[0])
        plassets.db.session.add(yagi2[0])
        plassets.db.session.commit()
        
        res = self.client.get('/assets/v1/sat')
        self.assertEqual(res.json,
                         [dove1[1], dove2[1], rapideye1[1], rapideye2[1]])
        
    def test_filter_dove(self):
        ''' Test retrieving only dove satellites.
        '''
        vecs = make_vectors()
        dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2 = vecs
        plassets.db.session.add(dove1[0])
        plassets.db.session.add(dove2[0])
        plassets.db.session.add(rapideye1[0])
        plassets.db.session.add(rapideye2[0])
        plassets.db.session.add(dish1[0])
        plassets.db.session.add(dish2[0])
        plassets.db.session.add(yagi1[0])
        plassets.db.session.add(yagi2[0])
        plassets.db.session.commit()
        
        res = self.client.get('/assets/v1/sat/dove')
        self.assertEqual(res.json,
                         [dove1[1], dove2[1]])
        
    def test_filter_rapideye(self):
        ''' Test retrieving only rapideye satellites.
        '''
        vecs = make_vectors()
        dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2 = vecs
        plassets.db.session.add(dove1[0])
        plassets.db.session.add(dove2[0])
        plassets.db.session.add(rapideye1[0])
        plassets.db.session.add(rapideye2[0])
        plassets.db.session.add(dish1[0])
        plassets.db.session.add(dish2[0])
        plassets.db.session.add(yagi1[0])
        plassets.db.session.add(yagi2[0])
        plassets.db.session.commit()
        
        res = self.client.get('/assets/v1/sat/rapideye')
        self.assertEqual(res.json,
                         [rapideye1[1], rapideye2[1]])
        
    def test_filter_ants(self):
        ''' Test retrieving only antennae.
        '''
        vecs = make_vectors()
        dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2 = vecs
        plassets.db.session.add(dove1[0])
        plassets.db.session.add(dove2[0])
        plassets.db.session.add(rapideye1[0])
        plassets.db.session.add(rapideye2[0])
        plassets.db.session.add(dish1[0])
        plassets.db.session.add(dish2[0])
        plassets.db.session.add(yagi1[0])
        plassets.db.session.add(yagi2[0])
        plassets.db.session.commit()
        
        res = self.client.get('/assets/v1/ant/')
        self.assertEqual(res.json,
                         [dish1[1], dish2[1], yagi1[1], yagi2[1]])
        
    def test_filter_dish(self):
        ''' Test retrieving only dish antennae.
        '''
        vecs = make_vectors()
        dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2 = vecs
        plassets.db.session.add(dove1[0])
        plassets.db.session.add(dove2[0])
        plassets.db.session.add(rapideye1[0])
        plassets.db.session.add(rapideye2[0])
        plassets.db.session.add(dish1[0])
        plassets.db.session.add(dish2[0])
        plassets.db.session.add(yagi1[0])
        plassets.db.session.add(yagi2[0])
        plassets.db.session.commit()
        
        res = self.client.get('/assets/v1/ant/dish')
        self.assertEqual(res.json,
                         [dish1[1], dish2[1]])
        
    def test_filter_yagi(self):
        ''' Test retrieving only yagi antennae.
        '''
        vecs = make_vectors()
        dove1, dove2, rapideye1, rapideye2, dish1, dish2, yagi1, yagi2 = vecs
        plassets.db.session.add(dove1[0])
        plassets.db.session.add(dove2[0])
        plassets.db.session.add(rapideye1[0])
        plassets.db.session.add(rapideye2[0])
        plassets.db.session.add(dish1[0])
        plassets.db.session.add(dish2[0])
        plassets.db.session.add(yagi1[0])
        plassets.db.session.add(yagi2[0])
        plassets.db.session.commit()
        
        res = self.client.get('/assets/v1/ant/yagi')
        self.assertEqual(res.json,
                         [yagi1[1], yagi2[1]])
        
        
class AssetTester(flask_testing.TestCase):
    ''' Ancillary testing for plassets assets to ensure they correctly
    deal with input.
    '''
    
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
    
    def test_bad_names(self):
        ''' Test some invalid names
        '''
        with self.assertRaises(ValueError):
            Asset('foo', 'satellite', 'dove')
        
        with self.assertRaises(ValueError):
            Asset('foo!', 'satellite', 'dove')
        
        with self.assertRaises(ValueError):
            Asset('foofoofoofoofoofoofoofoofoofoofoofoofoofoofoofoofoofoo' +
                  'foofoofoofo', 'satellite', 'dove')
    
    def test_bad_types(self):
        ''' Test some invalid types
        '''
        with self.assertRaises(ValueError):
            Asset('name', 'foo', 'dove')
        
        with self.assertRaises(ValueError):
            Asset('name', 2, 'dove')
    
    def test_bad_classes(self):
        ''' Test some invalid classes
        '''
        with self.assertRaises(ValueError):
            Asset('name', 'satellite', 'foo')
            
        with self.assertRaises(ValueError):
            Asset('name', 'satellite', 2)
            
    def test_repeat(self):
        ''' Test that repeated creation fails.
        '''
        asset = Asset('name', 'satellite', 'dove')
        plassets.db.session.add(asset)
        plassets.db.session.commit()
        
        # Also make sure mutation fails
        with self.assertRaises(AttributeError):
            asset.name = 'name2'
        
        with self.assertRaises(ValueError):
            asset = Asset('name', 'satellite', 'dove')
            
    def test_retrieve(self):
        ''' Test that retrieving objects works correctly (makes sure
        we didn't fiddle too much with sqlalchemy's innards).
        '''
        asset = Asset('name', 'satellite', 'dove')
        plassets.db.session.add(asset)
        plassets.db.session.commit()
        
        asset2 = Asset.query.get('name')
        self.assertEqual(asset.name, asset2.name)
        self.assertEqual(asset.asset_class, asset2.asset_class)
    
    def test_dove(self):
        ''' Test valid and invalid doves
        '''
        Asset('name', 'satellite', 'dove')
        
        # Test invalid details
        with self.assertRaises(AttributeError):
            Asset('name', 'satellite', 'dove', foo='bar')
        
    def test_rapideye(self):
        ''' Test valid and invalid rapideyes
        '''
        Asset('name', 'satellite', 'rapideye')
        
        # Test invalid details
        with self.assertRaises(AttributeError):
            Asset('name', 'satellite', 'rapideye', foo='bar')
        
    def test_dish(self):
        ''' Test valid and invalid dishes
        '''
        Asset('name', 'antenna', 'dish')
        Asset('name', 'antenna', 'dish', diameter=.5)
        Asset('name', 'antenna', 'dish', radome=False)
        Asset('name', 'antenna', 'dish', diameter=.5, radome=False)
        
        # Test invalid details
        with self.assertRaises(AttributeError):
            Asset('name', 'antenna', 'dish', foo='bar')
        with self.assertRaises(TypeError):
            Asset('name', 'antenna', 'dish', diameter='foo')
        with self.assertRaises(TypeError):
            Asset('name', 'antenna', 'dish', radome='foo')
        
    def test_yagi(self):
        ''' Test valid and invalid yagi
        '''
        Asset('name', 'antenna', 'yagi')
        Asset('name', 'antenna', 'yagi', gain=.5)
        
        # Test invalid details
        with self.assertRaises(AttributeError):
            Asset('name', 'antenna', 'yagi', foo='bar')
        with self.assertRaises(TypeError):
            Asset('name', 'antenna', 'yagi', gain='foo')


if __name__ == '__main__':
    unittest.main()
