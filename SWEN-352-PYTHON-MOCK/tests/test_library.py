import unittest
import json

from unittest.mock import Mock
from library import library, library_db_interface

class TestLibrary(unittest.TestCase):
    def setUp(self):
        library_db_interface.Patron = Mock() 
        self.lib = library.Library()
        self.addCleanup(self.lib.db.close_db)

        with open('tests_data/ebooks.txt', 'r') as f:
            self.books_data = json.loads(f.read())

    def test_is_ebook_true(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertTrue(self.lib.is_ebook('learning python'))

    def test_is_ebook_false(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertFalse(self.lib.is_ebook('not learning python'))

    def test_get_ebooks_count(self):
        self.lib.api.get_ebooks = Mock(return_value=self.books_data)
        self.assertEqual(self.lib.get_ebooks_count('learning python'), 8)

    def test_is_book_by_author_true(self):
        books_by_author = ['learning python']
        self.lib.api.books_by_author = Mock(return_value=books_by_author)
        self.assertTrue(self.lib.is_book_by_author('Mark Lutz', 'Learning Python'))

    def test_is_book_by_author_false(self):
        books_by_author = ['learning python']
        self.lib.api.books_by_author = Mock(return_value=books_by_author)
        self.assertFalse(self.lib.is_book_by_author('Mark Lutz', 'not Learning Python'))

    def test_get_languages_for_book(self):
        books_info = [{
            'title': 'Learning Python', 
            'publisher': ["O'Reilly", "O'Reilly Media, Inc.", 'Shroff Publishers & Distributors Pvt. Ltd.'], 
            'publish_year': [2004, 2008, 2003, 1999], 
            'language': ['eng']
            }]
        self.lib.api.get_book_info = Mock(return_value=books_info)
        self.assertEqual(self.lib.get_languages_for_book('Learning Python'), {'eng'})

    def test_register_patron(self):
        self.lib.db.insert_patron = Mock(return_value=1)
        self.assertEqual(self.lib.register_patron('Edward', 'Gutenbach', 31, 3201), 1)

    def test_is_patron_registered_true(self):
        self.lib.db.retrieve_patron = Mock(return_value=3201)
        self.assertTrue(self.lib.is_patron_registered(library_db_interface.Patron))

    def test_is_patron_registered_false(self):
        self.lib.db.retrieve_patron = Mock(return_value=None)
        self.assertFalse(self.lib.is_patron_registered(library_db_interface.Patron))

    def test_borrow_book(self):
        patron = library_db_interface.Patron()
        
        add_borrowed_book_mock = Mock()
        patron.add_borrowed_book = add_borrowed_book_mock

        update_patron_mock = Mock()
        self.lib.db.update_patron = update_patron_mock

        self.lib.borrow_book('learning python', patron)
        add_borrowed_book_mock.assert_called_with('learning python')
        update_patron_mock.assert_called_with(patron)

    def test_return_borrowed_book(self):
        patron = library_db_interface.Patron()

        return_borrowed_book_mock = Mock()
        patron.return_borrowed_book = return_borrowed_book_mock

        update_patron_mock = Mock()
        self.lib.db.update_patron = update_patron_mock

        self.lib.return_borrowed_book('learning python', patron)
        return_borrowed_book_mock.assert_called_with('learning python')
        update_patron_mock.assert_called_with(patron)
        
    def test_is_book_borrowed(self):
        patron = library_db_interface.Patron()
        patron.get_borrowed_books = Mock(return_value='learning python')
        self.assertTrue(self.lib.is_book_borrowed('learning python', patron))