from django.test import TestCase

# Create your tests here.
# tests/test_myapp.py
from django.test import TestCase
from .models import Author, Genre, Condition, Image, Book, BookInterest

class AuthorTestCase(TestCase):
    def test_model_creation(self):
        my_instance = Author.objects.create(name="Test Name")
        self.assertEqual(my_instance.name, "Test Name")

class GenreTestCase(TestCase):
    def test_model_creation(self):
        my_instance = Genre.objects.create(name="Test Name")
        self.assertEqual(my_instance.name, "Test Name")

class ConditionTestCase(TestCase):
    def test_model_creation(self):
        my_instance = Condition.objects.create(name="Test Name")
        self.assertEqual(my_instance.name, "Test Name")

class ImageTestCase(TestCase):
    def test_model_creation(self):
        my_instance = Image.objects.create(title="Test Name")
        self.assertEqual(my_instance.title, "Test Name")


from django.contrib.auth.models import User

class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data for the Book model
        cls.author = Author.objects.create(name='Test Author')
        cls.genre = Genre.objects.create(name='Test Genre')
        cls.condition = Condition.objects.create(name='Test Condition')
        cls.image = Image.objects.create(title='Test Image')
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.book = Book.objects.create(
            title='Test Book',
            author=cls.author,
            condition=cls.condition,
            Image=cls.image,
            owner=cls.user,
            pickup_location='Test Location',
        )

    def test_book_str(self):
        self.assertEqual(str(self.book), 'Test Book')

    def test_book_status_choices(self):
        choices = dict(self.book.STATUS_CHOICES)
        self.assertEqual(choices['available'], 'Available')
        self.assertEqual(choices['requested'], 'Requested')
        self.assertEqual(choices['unavailable'], 'Unavailable')

    def test_book_previous_owner_set_null(self):
        # Test that previous_owner is set to NULL when owner changes
        new_owner = User.objects.create_user(username='newuser', password='newpassword')
        self.book.owner = new_owner
        self.book.save()
        self.assertIsNone(self.book.previous_owner)

class BookInterestModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test data for the BookInterest model
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.author = Author.objects.create(name='Test Author')
        cls.condition = Condition.objects.create(name='Test Condition')
        cls.image = Image.objects.create(title='Test Image')
        cls.book = Book.objects.create(
            title='Test Book',
            author=cls.author,
            condition=cls.condition,
            Image=cls.image,
            owner=cls.user,
            pickup_location='Test Location',
        )
        cls.book_interest = BookInterest.objects.create(
            interested_user=cls.user,
            book=cls.book,
        )

    def test_book_interest_str(self):
        self.assertEqual(str(self.book_interest), 'Test Book - testuser')