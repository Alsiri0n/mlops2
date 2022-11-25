"""
Tests for application
"""
import unittest
# from config import TestingConfig
from app import create_app, db
from app.models import Category, Product 


# class TestConfig(Config):
#     """
#     Creating test envs
#     """
#     TESTING = True
#     DB_URL = 'sqlite:///app.db'


class TestMLOPS(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
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

    
    def test_api_product(self):
        prod_temp_name="TEST_PROD_NAME"
        prod = Product(prod_name=prod_temp_name)

        db.session.add(prod)
        db.session.commit()

        prod_id = Product.query.filter_by(prod_name=prod_temp_name).first()
        resp = self.client.get(f'/api/products/{str(prod_id.id)}')

        js = resp.json
        self.assertEqual(resp.status_code, 200)
        self.assertIn(prod_temp_name, js['prod_name'])



    def test_api_category(self):
        cat_temp_name="TEST_CAT_NAME"
        cat = Category(cat_name=cat_temp_name)
        
        db.session.add(cat)
        db.session.commit()

        cat_id = Category.query.filter_by(cat_name=cat_temp_name).first()
        resp = self.client.get(f'/api/categories/{str(cat_id.id)}')
        js = resp.json

        self.assertEqual(resp.status_code, 200)
        self.assertIn(cat_temp_name, js['cat_name'])


    def test_api_product_in_category(self):
        prod_temp_name="TEST_PROD_NAME"
        cat_temp_name="TEST_CAT_NAME"
        prod = Product(prod_name=prod_temp_name)
        cat = Category(cat_name=cat_temp_name)

        db.session.add(prod)
        db.session.add(cat)
        db.session.commit()

        prod_id = Product.query.filter_by(prod_name=prod_temp_name).first()
        cat_id = Category.query.filter_by(cat_name=cat_temp_name).first()
        prod.categories.append(cat_id)
        db.session.commit()
        resp = self.client.get(f'/api/products/{str(prod_id.id)}/categories')

        js = resp.json['items'][0]
        self.assertEqual(resp.status_code, 200)
        self.assertIn(cat_temp_name, js['cat_name'])


    def test_api_category_in_product(self):
        prod_temp_name="TEST_PROD_NAME"
        cat_temp_name="TEST_CAT_NAME"
        prod = Product(prod_name=prod_temp_name)
        cat = Category(cat_name=cat_temp_name)

        db.session.add(prod)
        db.session.add(cat)
        db.session.commit()

        prod_id = Product.query.filter_by(prod_name=prod_temp_name).first()
        cat_id = Category.query.filter_by(cat_name=cat_temp_name).first()
        prod.categories.append(cat_id)
        db.session.commit()
        resp = self.client.get(f'/api/categories/{str(cat_id.id)}/products')

        js = resp.json['items'][0]
        self.assertEqual(resp.status_code, 200)
        self.assertIn(prod_temp_name, js['prod_name'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
