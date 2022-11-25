"""
Describe all models at test case
"""
from app import db
from flask import url_for


# class PaginatedAPIMixin(object):
#     """
#     For convient work with collection of items
#     """
#     @staticmethod
#     def to_collection_dict(query, page:int, per_page:int, endpoint:str,
#                             full_data:bool=False, **kwargs)->dict:
#         """
#         Generic method for convert query to dict
#         """
#         resources = db.paginate(select=query, per_page=per_page, error_out=False)
#         data = {
#             'items': [item.to_dict(endpoint, full_data) for item in resources.items],
#             '_meta': {
#                 'page': page,
#                 'per_page': per_page,
#                 'total_pages': resources.pages,
#                 'total_items': resources.total
#             },
#             '_links': {
#                 'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
#                 'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs ) \
#                                 if resources.has_next else None,
#                 'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) \
#                                 if resources.has_prev else None
#             }
#         }
#         return data



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
                                backref=db.backref('products', lazy='dynamic'), lazy='dynamic')

    def __repr__(self)->str:
        return f'<Product id={self.id} prod_name={self.prod_name}>'


    @staticmethod
    def full_dict(query, endpoint:str, **kwargs)->dict:
        resources = db.paginate(select=query, per_page=100, error_out=False)
        data = {
            'items': [item.to_dict(endpoint, True) for item in resources.items],
        }
        return data

    def to_dict(self, endpoint:str, full_dict:bool=False)->dict:
        """
        Return dict that represents Product for JSON serialization
        """
        if full_dict:
            fulldata = db.paginate(select=db.select(Category).\
                join(Category.products).where(Product.id==self.id),
                 per_page=10, error_out=False)
            data = {
                'id': self.id,
                'prod_name': self.prod_name,

                'categories': [item.to_dict(endpoint, False) for item in fulldata.items],
                '_links': {
                    'self': url_for(endpoint='api.get_product', id=self.id),
    
                }
            }
        else: 
            data = {
                'id': self.id,
                'prod_name': self.prod_name,
                '_links': {
                    'self': url_for(endpoint='api.get_product', id=self.id),
                }
            }
        return data



class Category(db.Model):
    """
    Model for Category
    """
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    cat_name = db.Column(db.String(50), unique=True)

    def __repr__(self)->str:
        return f'<Category id={self.id}, cat_name={self.cat_name}>'


    @staticmethod
    def full_dict(query, endpoint:str, **kwargs)->dict:
        resources = db.paginate(select=query, per_page=100, error_out=False)
        data = {
            'items': [item.to_dict(endpoint, True) for item in resources.items],
        }
        return data


    def to_dict(self, endpoint:str, full_dict:bool=False)->dict:
        """
        Return dict that represents Category for JSON serialization
        """
        if full_dict:
            fulldata = db.paginate(select=db.select(Product).\
                join(Product.categories).where(Category.id==self.id),
                 per_page=10, error_out=False)
            data = {
                'id': self.id,
                'cat_name': self.cat_name,

                'products': [item.to_dict(endpoint, False) for item in fulldata.items],
                '_links': {
                    'self': url_for(endpoint='api.get_category', id=self.id),
                }
            }
        else:
            data = {
                'id': self.id,
                'cat_name': self.cat_name,
                '_links': {
                    'self': url_for(endpoint=endpoint, id=self.id),
                }
            }
        return data
