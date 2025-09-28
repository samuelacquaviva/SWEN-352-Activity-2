import unittest
from library import ext_api_interface
from unittest.mock import Mock
import requests
import json

class TestExtApiInterface(unittest.TestCase):
    def setUp(self):
        self.api = ext_api_interface.Books_API()
        self.book = "learning python"
        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())
        with open('tests_data/json_data.txt', 'r') as f:
            self.json_data = json.loads(f.read())

    def test_make_request_True(self):
        attr = {'json.return_value': dict()}
        requests.get = Mock(return_value = Mock(status_code = 200, **attr))
        self.assertEqual(self.api.make_request(""), dict())

    def test_make_request_connection_error(self):
        ext_api_interface.requests.get = Mock(side_effect=requests.ConnectionError)
        url = "some url"
        self.assertEqual(self.api.make_request(url), None)

    def test_make_request_False(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(self.api.make_request(""), None)

    def test_get_ebooks(self):
        self.api.make_request = Mock(return_value=self.json_data)
        self.assertEqual(self.api.get_ebooks(self.book), self.books_data)
    
    def test_get_ebooks_empty(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(self.api.get_ebooks(self.book), [])
    
    def test_is_book_available_True(self):
        self.api.make_request = Mock(return_value = self.json_data)
        self.assertEqual(self.api.is_book_available(self.book), True)
    
    def test_is_book_available_False(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(self.api.is_book_available("Fake Book"), False)
    
    def test_books_by_author_valid(self):
        self.api.make_request = Mock(return_value = self.json_data)
        self.assertEqual(len(self.api.books_by_author("Mark Lutz")), 100)
    
    def test_books_by_author_invalid(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(len(self.api.books_by_author("Fake Author")), 0)
    
    def test_get_book_info_valid(self):
        self.api.make_request = Mock(return_value = self.json_data)
        self.assertEqual(len(self.api.get_book_info(self.book)), 100)
    
    def test_get_book_info_invalid(self):
        requests.get = Mock(return_value=Mock(status_code=100))
        self.assertEqual(len(self.api.get_book_info("Fake Book")), 0)