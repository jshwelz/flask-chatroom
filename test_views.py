import unittest
import coverage
import json
from flask import Flask
from flask_socketio import SocketIO
from app.views import *


class TestSocketIO(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_connect(self):               
        client = socketio.test_client(app)
        self.assertTrue(client.is_connected())
        received = client.get_received()               
        client.disconnect()
        self.assertFalse(client.is_connected())


    def test_post_message(self):
        client = socketio.test_client(app)                
        client.emit('event', {'user_name': 'John', 'message':'Hello'})
        received = client.get_received()              
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['name'], 'response')
        self.assertEqual(received[0]['args'][0]['user_name'], 'John')

    def test_get_stock(self):
        client = socketio.test_client(app)                
        client.emit('event', {'user_name': 'John', 'message':'/stock=aapl.us'})
        received = client.get_received()                
        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]['name'], 'response')
        self.assertNotEqual(received[0]['args'][0]['user_name'], 'John')
        self.assertEqual(received[0]['args'][0]['user_name'], 'bot')
        client.emit('event', {'user_name': 'John', 'message':'/stock=11'})
        received = client.get_received()          
        self.assertEqual(len(received), 0)




if __name__ == '__main__':
    unittest.main()
