#Imports

import unittest
from flask_testing import TestCase
from flask_login import current_user
from project import app, db
from project.models import User, BlogPost

class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User("admin", "admin@domain.com", "admin"))
        db.session.add(BlogPost("Test post", "This is a test. Only a test.", "admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):
    # Ensure Flask is set-up correctly
    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_main_route_requires_login(self):
        response = self.client.get('/',follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_posts_on_main_page(self):
        response = self.client.post(
            '/login',
            data=dict(username='admin', password='admin'),
            follow_redirects=True
        )
        self.assertIn(b'This is a test. Only a test.', response.data)


class UsersViewsTests(BaseTestCase):
    # Ensure login page loads correctly.
    def test_login_page(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # TestCase for correct login credentials
    def test_login_correct_credentials(self):
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(username='admin', password='admin'),
                follow_redirects=True)
            self.assertIn(b'You were just logged in', response.data)
            self.assertTrue(current_user.name == 'admin')
            self.assertTrue(current_user.is_active())

    # TestCase for incorrect login credentials
    def test_login_incorrect_credentials(self):
        response = self.client.post(
            '/login',
            data=dict(username='admin', password='adin'),
            follow_redirects=True
        )
        self.assertIn(b'Invalid Credentials', response.data)

    # TestCase for logout.
    def test_logout(self):
        with self.client:
            self.client.post(
                '/login',
                data=dict(username='admin', password='admin'),
                follow_redirects=True
            )
            response = self.client.get('/logout', follow_redirects=True)
            self.assertIn(b'You were just logged out', response.data)
            self.assertFalse(current_user.is_active())

    # TestCase for correct login credentials
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/register',
                data=dict(username='testing', email='email@email.com',
                            password='testing', confirm='testing'),
                follow_redirects=True)
            self.assertIn(b'Welcome to Flask', response.data)
            self.assertTrue(current_user.name == 'testing')
            self.assertTrue(current_user.is_active())



if __name__ == '__main__':
  unittest.main()
