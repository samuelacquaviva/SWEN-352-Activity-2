import unittest
from unittest.mock import Mock, call
from library import library_db_interface


class TestLibraryDBInterface(unittest.TestCase):
    
    def setUp(self):
        self.db_interface = library_db_interface.Library_DB()
    
    def test_insert_patron_not_in_db(self):
        patron_mock = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=None)
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(side_effect=lambda x: 10 if x==data else 0)
        self.assertEqual(self.db_interface.insert_patron(patron_mock), 10)
    
    def test_insert_patron_none(self):
        result = self.db_interface.insert_patron(None)
        self.assertIsNone(result)
    
    def test_insert_patron_already_in_db(self):
        patron_mock = Mock()
        existing_patron = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=existing_patron)
        result = self.db_interface.insert_patron(patron_mock)
        self.assertIsNone(result)
    
    def test_get_patron_count(self):
        mock_results = [{'memberID': '1'}, {'memberID': '2'}, {'memberID': '3'}]
        self.db_interface.db.all = Mock(return_value=mock_results)
        self.assertEqual(self.db_interface.get_patron_count(), 3)
    
    def test_get_all_patrons(self):
        mock_results = [{'memberID': '1'}, {'memberID': '2'}]
        self.db_interface.db.all = Mock(return_value=mock_results)
        self.assertEqual(self.db_interface.get_all_patrons(), mock_results)
    
    def test_update_patron(self):
        data = {'fname': 'name', 'lname': 'name', 'age': 'age', 'memberID': 'memberID',
                'borrowed_books': []}
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock()
        self.db_interface.db.update = db_update_mock
        self.db_interface.update_patron(Mock())
        db_update_mock.assert_called()
    
    def test_update_patron_none(self):
        result = self.db_interface.update_patron(None)
        self.assertIsNone(result)
    
    def test_retrieve_patron_found(self):
        mock_results = [{'fname': 'John', 'lname': 'Doe', 'age': 30, 'memberID': '123'}]
        self.db_interface.db.search = Mock(return_value=mock_results)
        result = self.db_interface.retrieve_patron('123')
        self.assertIsNotNone(result)
        self.db_interface.db.search.assert_called()
    
    def test_retrieve_patron_not_found(self):
        self.db_interface.db.search = Mock(return_value=[])
        result = self.db_interface.retrieve_patron('999')
        self.assertIsNone(result)
    
    def test_close_db(self):
        db_close_mock = Mock()
        self.db_interface.db.close = db_close_mock
        self.db_interface.close_db()
        db_close_mock.assert_called()
    
    def test_convert_patron_to_db_format(self):
        patron_mock = Mock()
        patron_mock.get_fname = Mock(return_value=1)
        patron_mock.get_lname = Mock(return_value=2)
        patron_mock.get_age = Mock(return_value=3)
        patron_mock.get_memberID = Mock(return_value=4)
        patron_mock.get_borrowed_books = Mock(return_value=5)
        self.assertEqual(self.db_interface.convert_patron_to_db_format(patron_mock),
                         {'fname': 1, 'lname': 2, 'age': 3, 'memberID': 4,
                          'borrowed_books': 5})

