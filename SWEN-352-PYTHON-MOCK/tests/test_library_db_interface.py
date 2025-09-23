import unittest
from unittest.mock import Mock, patch
from library import library_db_interface
from library.patron import Patron


class TestLibraryDBInterface(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Mock TinyDB to avoid actual database operations
        self.mock_db_patcher = patch('library.library_db_interface.TinyDB')
        self.mock_tinydb = self.mock_db_patcher.start()
        self.mock_db_instance = Mock()
        self.mock_tinydb.return_value = self.mock_db_instance
        
        # Create the database interface instance
        self.db_interface = library_db_interface.Library_DB()
        
        # Create mock patron for testing
        self.mock_patron = Mock(spec=Patron)
        self.mock_patron.get_memberID.return_value = "12345"
        self.mock_patron.get_fname.return_value = "John"
        self.mock_patron.get_lname.return_value = "Doe"
        self.mock_patron.get_age.return_value = 30
        self.mock_patron.get_borrowed_books.return_value = ["Book1", "Book2"]
    
    def tearDown(self):
        """Clean up after each test method."""
        self.mock_db_patcher.stop()
    
    def test_init_creates_tinydb_instance(self):
        """Test that __init__ creates a TinyDB instance with correct file."""
        # TinyDB should be called with the DATABASE_FILE
        self.mock_tinydb.assert_called_with('db.json')
        # The db attribute should be set to the mock instance
        self.assertEqual(self.db_interface.db, self.mock_db_instance)
    
    def test_insert_patron_success(self):
        """Test successful patron insertion."""
        # Mock that patron doesn't exist in DB
        self.db_interface.retrieve_patron = Mock(return_value=None)
        # Mock the insert operation
        self.mock_db_instance.insert.return_value = 1
        
        result = self.db_interface.insert_patron(self.mock_patron)
        
        # Verify the patron was checked first
        self.db_interface.retrieve_patron.assert_called_once_with("12345")
        # Verify insert was called with correct data
        expected_data = {
            'fname': 'John',
            'lname': 'Doe',
            'age': 30,
            'memberID': '12345',
            'borrowed_books': ['Book1', 'Book2']
        }
        self.mock_db_instance.insert.assert_called_once_with(expected_data)
        self.assertEqual(result, 1)
    
    def test_insert_patron_none_parameter(self):
        """Test insert_patron with None parameter."""
        result = self.db_interface.insert_patron(None)
        self.assertIsNone(result)
        self.mock_db_instance.insert.assert_not_called()
    
    def test_insert_patron_already_exists(self):
        """Test insert_patron when patron already exists in database."""
        # Mock that patron already exists
        existing_patron = Mock()
        self.db_interface.retrieve_patron = Mock(return_value=existing_patron)
        
        result = self.db_interface.insert_patron(self.mock_patron)
        
        # Should return None and not call insert
        self.assertIsNone(result)
        self.mock_db_instance.insert.assert_not_called()
    
    def test_get_patron_count(self):
        """Test getting patron count from database."""
        # Mock the database return value
        mock_patrons = [{'memberID': '1'}, {'memberID': '2'}, {'memberID': '3'}]
        self.mock_db_instance.all.return_value = mock_patrons
        
        result = self.db_interface.get_patron_count()
        
        self.mock_db_instance.all.assert_called_once()
        self.assertEqual(result, 3)
    
    def test_get_all_patrons(self):
        """Test getting all patrons from database."""
        mock_patrons = [
            {'memberID': '1', 'fname': 'John'},
            {'memberID': '2', 'fname': 'Jane'}
        ]
        self.mock_db_instance.all.return_value = mock_patrons
        
        result = self.db_interface.get_all_patrons()
        
        self.mock_db_instance.all.assert_called_once()
        self.assertEqual(result, mock_patrons)
    
    @patch('library.library_db_interface.Query')
    def test_update_patron_success(self, mock_query_class):
        """Test successful patron update."""
        # Mock Query class
        mock_query = Mock()
        mock_query_class.return_value = mock_query
        mock_condition = Mock()
        mock_query.memberID = Mock()
        mock_query.memberID.__eq__ = Mock(return_value=mock_condition)
        
        result = self.db_interface.update_patron(self.mock_patron)
        
        # Verify update was called with correct data and condition
        expected_data = {
            'fname': 'John',
            'lname': 'Doe',
            'age': 30,
            'memberID': '12345',
            'borrowed_books': ['Book1', 'Book2']
        }
        self.mock_db_instance.update.assert_called_once_with(expected_data, mock_condition)
        # Should return None (void method)
        self.assertIsNone(result)
    
    def test_update_patron_none_parameter(self):
        """Test update_patron with None parameter."""
        result = self.db_interface.update_patron(None)
        
        self.assertIsNone(result)
        self.mock_db_instance.update.assert_not_called()
    
    @patch('library.library_db_interface.Query')
    @patch('library.library_db_interface.Patron')
    def test_retrieve_patron_found(self, mock_patron_class, mock_query_class):
        """Test retrieving an existing patron."""
        # Mock Query class
        mock_query = Mock()
        mock_query_class.return_value = mock_query
        mock_condition = Mock()
        mock_query.memberID = Mock()
        mock_query.memberID.__eq__ = Mock(return_value=mock_condition)
        
        # Mock database search result
        mock_search_result = [{
            'fname': 'John',
            'lname': 'Doe',
            'age': 30,
            'memberID': '12345'
        }]
        self.mock_db_instance.search.return_value = mock_search_result
        
       
        mock_patron_instance = Mock()
        mock_patron_class.return_value = mock_patron_instance
        
        result = self.db_interface.retrieve_patron("12345")
        
        
        self.mock_db_instance.search.assert_called_once_with(mock_condition)
        mock_patron_class.assert_called_once_with('John', 'Doe', 30, '12345')
        self.assertEqual(result, mock_patron_instance)
    
    @patch('library.library_db_interface.Query')
    def test_retrieve_patron_not_found(self, mock_query_class):
        """Test retrieving a non-existing patron."""
       
        mock_query = Mock()
        mock_query_class.return_value = mock_query
        mock_condition = Mock()
        mock_query.memberID = Mock()
        mock_query.memberID.__eq__ = Mock(return_value=mock_condition)
        
      
        self.mock_db_instance.search.return_value = []
        
        result = self.db_interface.retrieve_patron("99999")
        
        self.mock_db_instance.search.assert_called_once_with(mock_condition)
        self.assertIsNone(result)
    
    def test_close_db(self):
        """Test closing the database."""
        self.db_interface.close_db()
        self.mock_db_instance.close.assert_called_once()
    
    def test_convert_patron_to_db_format(self):
        """Test converting patron object to database format."""
        result = self.db_interface.convert_patron_to_db_format(self.mock_patron)
        
        expected_result = {
            'fname': 'John',
            'lname': 'Doe',
            'age': 30,
            'memberID': '12345',
            'borrowed_books': ['Book1', 'Book2']
        }
        
       
        self.mock_patron.get_fname.assert_called_once()
        self.mock_patron.get_lname.assert_called_once()
        self.mock_patron.get_age.assert_called_once()
        self.mock_patron.get_memberID.assert_called_once()
        self.mock_patron.get_borrowed_books.assert_called_once()
        
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
   
    unittest.main()