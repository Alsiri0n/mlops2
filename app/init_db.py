import random
import string
from app import db
from app.models import Category, Product

CATEGORY_QNT = 10
PRODUCT_QNT = 50


def clear_data():
    db.drop_all()
    db.create_all()


def dummy_data():
    clear_data()

    categories = []
    products = []
    for _ in range(CATEGORY_QNT):
        categories.append(Category(cat_name=''.join(random.choices(string.ascii_lowercase, k=7))))

    for _ in range(PRODUCT_QNT):
        products.append(Product(prod_name=''.join(random.choices(string.ascii_lowercase, k=15))))

    for product in products[:-5]:
        product.categories.extend(random.choices(categories[:-1], k=random.choice([1,2,3])))

    db.session.add_all(categories)
    db.session.add_all(products)

    db.session.commit()
