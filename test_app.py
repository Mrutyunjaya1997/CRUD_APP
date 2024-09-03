import unittest
import sqlite3
from app import app, get_db_connection

class SimpleFlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test_database.db'
        self.app = app.test_client()
        # Set up a test database
        conn = get_db_connection()
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)')
        conn.close()

    def tearDown(self):
        # Remove the test database
        conn = get_db_connection()
        conn.execute('DROP TABLE IF EXISTS users')
        conn.close()

    def test_add_user(self):
        """
        Test that a new user can be added successfully.
        """
        response = self.app.post('/add/', data=dict(name="John Doe", email="john@example.com"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check if the user was added to the database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE name = 'John Doe' AND email = 'john@example.com'")
        user = cur.fetchone()
        conn.close()
        self.assertIsNotNone(user)  # Ensure the user exists

if __name__ == '__main__':
    unittest.main()
