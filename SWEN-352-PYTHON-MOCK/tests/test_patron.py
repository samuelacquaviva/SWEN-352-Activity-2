import unittest
from library import patron

class TestPatron(unittest.TestCase):

  def setUp(self):
      self.pat = patron.Patron('John', 'Doe', '25', '1001')

  def test_valid_name(self):
      pat = patron.Patron('John', 'Doe', '25', '1001')
      self.assertTrue(isinstance(pat, patron.Patron))

  def test_invalid_name(self):
      self.assertRaises(patron.InvalidNameException, patron.Patron, 'J0hn', 'Doe', '25', '1003')

  def test_add_borrowed_book(self):
      self.pat.add_borrowed_book("Book A")
      self.assertIn("book a", self.pat.get_borrowed_books())

  def test_add_duplicate_book(self):
      self.pat.add_borrowed_book("Book A")
      self.pat.add_borrowed_book("Book A")  # duplicate
      self.assertEqual(len(self.pat.get_borrowed_books()), 1)

  def test_return_borrowed_book(self):
      self.pat.add_borrowed_book("Book A")
      self.pat.return_borrowed_book("Book A")
      self.assertNotIn("book a", self.pat.get_borrowed_books())

  def test_return_nonexistent_book(self):
      self.pat.return_borrowed_book("Book Z")
      self.assertEqual(self.pat.get_borrowed_books(), [])

  def test_getters(self):
      self.assertEqual(self.pat.get_fname(), "John")
      self.assertEqual(self.pat.get_lname(), "Doe")
      self.assertEqual(self.pat.get_age(), "25")
      self.assertEqual(self.pat.get_memberID(), "1001")

  def test_equality(self):
      pat2 = patron.Patron('John', 'Doe', '25', '1001')
      self.assertEqual(self.pat, pat2)

  def test_inequality(self):
      pat2 = patron.Patron('Jane', 'Doe', '25', '1001')
      self.assertNotEqual(self.pat, pat2)



