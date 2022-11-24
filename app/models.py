"""
Describe all models at test case
"""
from app import db
from flask import url_for


class PaginatedAPIMixin(object):
    """
    For convient work with collection of items
    """
    @staticmethod
    def to_collection_dict(query, page:int, per_page:int, endpoint:str, **kwargs)->dict:
        """
        Generic method for convert query to dict
        """
        resources = query.paginate(page=page, per_page=per_page, error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs ) \
                                if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) \
                                if resources.has_prev else None
            }
        }
        return data



products_categories = db.Table('products_categories',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id')))


class Product(PaginatedAPIMixin, db.Model):
    """
    Represent model for Product
    """
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    prod_name = db.Column(db.String(50))

    categories = db.relationship("Category", secondary=products_categories,
                                backref=db.backref('products', lazy='dynamic'), lazy='dynamic')

    def __repr__(self)->str:
        return f'<Product id={self.id} prod_name={self.prod_name}>'

    def to_dict(self):
        """
        Return dict that represents Product for JSON serialization
        """
        data = {
            'id': self.id,
            'prod_name': self.prod_name,
            '_links': {
                'self': url_for('api.get_product', id=self.id),
                # 'categories': url_for('api.get_followers', id=self.id),
            }
        }
        return data



class Category(PaginatedAPIMixin, db.Model):
    """
    Model for Category
    """
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(50), unique=True)

    # products = db.relationship("Product", secondary=products_categories,
    #                             backref=db.backref('entity', lazy='dynamic'), lazy='dynamic')
    def __repr__(self)->str:
        return f'<Category id={self.id}, cat_name={self.cat_name}>'

    def to_dict(self):
        """
        Return dict that represents Product for JSON serialization
        """
        data = {
            'id': self.id,
            'cat_name': self.cat_name,
            '_links': {
                'self': url_for('api.get_category', id=self.id),
                # 'categories': url_for('api.get_followers', id=self.id),
            }
        }
        return data