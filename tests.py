"""
Tests for application
"""
import unittest
from config import Config
from app import create_app, db
from app.models import Category, Product 


class TestConfig(Config):
    """
    Creating test envs
    """
    TESTING = True
    DB_URL = 'sqlite:///app.db'


class TestMLOPS(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index(self):
        """
        Check index page
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        html = resp.data.decode()
        self.assertIn("reset", html)
        self.assertIn("populate", html)


    def test_populate_data(self):
        resp = self.client.post('/', data=dict(populate='Reset and populate'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Category.query.count(), 10)
        self.assertEqual(Product.query.count(), 50)

    def test_reset_data(self):
        self.client.post('/', data=dict(reset='Reset'))
        self.assertEqual(Category.query.count(), 0)
        self.assertEqual(Product.query.count(), 0)

    def test_product_without_category(self):
        """
            SELECT p.id as p_id,
                   p.prod_name,
                   c.id as cat_id,
                   c.cat_name,
                   COUNT(p.id)
              FROM product p
                        LEFT JOIN products_categories pc ON p.id = pc.product_id
                        LEFT JOIN category c ON pc.category_id = c.id
             WHERE c.cat_name is NULL
             GROUP BY 1,2,3,4;
        """
        resp = self.client.post('/', data=dict(populate='Reset and populate'))
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(Product.query.filter(~Product.categories.any()).all(), 0)


    def test_category_without_product(self):
        """
            SELECT p.id as p_id,
                   p.prod_name,
                   c.id as cat_id,
                   c.cat_name,
                   COUNT(c.id)
              FROM category c
                        LEFT JOIN products_categories pc ON c.id = pc.category_id
                        LEFT JOIN product p ON pc.product_id = p.id
             WHERE p.prod_name is NULL
             GROUP BY 1,2,3,4;
        """
        resp = self.client.post('/', data=dict(populate='Reset and populate'))
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(Category.query.filter(~Category.products.any()).count(), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
