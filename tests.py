"""
Tests for application
"""
import unittest
from app import create_app, db
from app.models import Category, Product


DEFAULT_CAT_QNT = 10
DEFAULT_PROD_QNT = 50
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
        """
        Test html button for check populate base
        """
        resp = self.client.post('/', data=dict(populate='Reset and populate'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Category.query.count(), DEFAULT_CAT_QNT)
        self.assertEqual(Product.query.count(), DEFAULT_PROD_QNT)


    def test_reset_data(self):
        """
        Check html button for check clear base
        """
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
        """
        Create new product and check through API exists.
        """
        db.drop_all()
        db.create_all()
        prod_temp_name="TEST_PROD_NAME"
        prod = Product(prod_name=prod_temp_name)

        db.session.add(prod)
        db.session.commit()

        prod_id = Product.query.filter_by(prod_name=prod_temp_name).first()
        resp = self.client.get(f'/api/products/{str(prod_id.id)}')

        data_js = resp.json
        self.assertEqual(resp.status_code, 200)
        self.assertIn(prod_temp_name, data_js['prod_name'])



    def test_api_category(self):
        """
        Create new category and check through API exists.
        """
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
        """
        Check main logic.
        Create new product, category and append category to product.
        """
        db.drop_all()
        db.create_all()
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

        data_js = resp.json['items'][0]
        self.assertEqual(resp.status_code, 200)
        self.assertIn(cat_temp_name, data_js['cat_name'])


    def test_api_category_in_product(self):
        """
        Check main logic.
        Create new product, category and append category to product.
        """
        db.drop_all()
        db.create_all()
        prod_temp_name="TEST_PROD_NAME"
        cat_temp_name="TEST_CAT_NAME"
        prod = Product(prod_name=prod_temp_name)
        cat = Category(cat_name=cat_temp_name)

        db.session.add(prod)
        db.session.add(cat)
        db.session.commit()

        cat_id = Category.query.filter_by(cat_name=cat_temp_name).first()
        prod.categories.append(cat_id)
        db.session.commit()
        resp = self.client.get(f'/api/categories/{str(cat_id.id)}/products')

        data_js = resp.json['items'][0]
        self.assertEqual(resp.status_code, 200)
        self.assertIn(prod_temp_name, data_js['prod_name'])


    def test_all_products_in_cat(self):
        """
        Check products belongs category
        """
        db.drop_all()
        db.create_all()
        prod_temp_name1="TEST_PROD_NAME1"
        cat_temp_name1="TEST_CAT_NAME1"
        prod_temp_name2="TEST_PROD_NAME2"
        cat_temp_name2="TEST_CAT_NAME2"
        prod1 = Product(prod_name=prod_temp_name1)
        cat1 = Category(cat_name=cat_temp_name1)
        prod2 = Product(prod_name=prod_temp_name2)
        cat2 = Category(cat_name=cat_temp_name2)

        db.session.add(prod1)
        db.session.add(prod2)
        db.session.add(cat1)
        db.session.add(cat2)
        db.session.commit()

        cat_id1 = Category.query.filter_by(cat_name=cat_temp_name1).first()
        cat_id2 = Category.query.filter_by(cat_name=cat_temp_name2).first()

        #Append prod1 and prod2 to cat1
        prod1.categories.append(cat_id1)
        prod2.categories.append(cat_id1)
        db.session.commit()
        resp = self.client.get(f'/api/categories/{str(cat_id1.id)}/products')
        data_js = resp.json

        #Check cat1
        self.assertEqual(resp.status_code, 200)
        self.assertIn(cat_temp_name1, data_js['items'][0]['categories'][0]['cat_name'])
        self.assertIn(prod_temp_name1, data_js['items'][0]['prod_name'])
        self.assertIn(prod_temp_name2, data_js['items'][1]['prod_name'])
        self.assertNotIn(cat_temp_name2, data_js['items'][0]['categories'][0]['cat_name'])

        #Check cat2
        resp = self.client.get(f'/api/categories/{str(cat_id2.id)}/products')
        data_js = resp.json
        self.assertEqual(resp.status_code, 200)
        self.assertEqual({'items': []}, data_js)


    def test_all_categories_in_prod(self):
        """
        Check categories belongs product
        """
        db.drop_all()
        db.create_all()
        prod_temp_name1="TEST_PROD_NAME1"
        prod_temp_name2="TEST_PROD_NAME2"
        cat_temp_name1="TEST_CAT_NAME1"
        cat_temp_name2="TEST_CAT_NAME2"
        prod1 = Product(prod_name=prod_temp_name1)
        prod2 = Product(prod_name=prod_temp_name2)
        cat1 = Category(cat_name=cat_temp_name1)
        cat2 = Category(cat_name=cat_temp_name2)

        db.session.add(prod1)
        db.session.add(prod2)
        db.session.add(cat1)
        db.session.add(cat2)
        db.session.commit()

        prod_id1 = Product.query.filter_by(prod_name=prod_temp_name1).first()
        prod_id2 = Product.query.filter_by(prod_name=prod_temp_name2).first()
        cat_id1 = Category.query.filter_by(cat_name=cat_temp_name1).first()
        cat_id2 = Category.query.filter_by(cat_name=cat_temp_name2).first()

        #Append cat1 and cat2 to prod1
        cat1.products.append(prod1)
        cat2.products.append(prod1)
        db.session.commit()
        resp = self.client.get(f'/api/products/{str(prod_id1.id)}/categories')
        data_js = resp.json

        #Check prod1
        self.assertEqual(resp.status_code, 200)
        self.assertIn(prod_temp_name1, data_js['items'][0]['products'][0]['prod_name'])
        self.assertIn(prod_temp_name1, data_js['items'][1]['products'][0]['prod_name'])


        #Check prod2
        resp = self.client.get(f'/api/products/{str(cat_id2.id)}/categories')
        data_js = resp.json
        self.assertEqual(resp.status_code, 200)
        self.assertEqual({'items': []}, data_js)

if __name__ == '__main__':
    unittest.main(verbosity=2)
