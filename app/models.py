"""
Describe all models at test case
"""
from app import db



products_categories = db.Table('products_categories',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')))


class Product(db.Model):
    """
    Represent model for Product
    """
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(50))

    categories = db.relationship("Category", secondary=products_categories,
                                backref=db.backref('type', lazy='dynamic'), lazy='dynamic')


class Category(db.Model):
    """
    Model for Category
    """
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(50), unique=True)

    # products = db.relationship("Product", secondary=products_categories,
    #                             backref=db.backref('entity', lazy='dynamic'), lazy='dynamic')
