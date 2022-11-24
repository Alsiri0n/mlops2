from app.api import bp
from app.api.errors import bad_request
from flask import jsonify, request, url_for, abort, request
from app import db
from app.models import Product, Category


@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id:int):
    """
    Return product by id
    """
    return jsonify(Product.query.get_or_404(id).to_dict())


@bp.route('/products', methods=['GET'])
def get_products():
    """
    Return all products
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Product.to_collection_dict(Product.query, page, per_page, 'api.get_products')
    return jsonify(data)


@bp.route('/products/<int:id>/categories', methods=['GET'])
def get_categories_for_product(id:int):
    """
    Return categories for product
    """
    product = Product.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 2, type=int), 100)
    data = Product.to_collection_dict(product.categories, page, per_page, 
                                    'api.get_categories_for_product', id=id)
    return jsonify(data)


@bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id:int):
    """
    Return category by id
    """
    return jsonify(Category.query.get_or_404(id).to_dict())

@bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Return all categories
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 3, type=int), 100)
    data = Category.to_collection_dict(Category.query, page, per_page, 'api.get_categories')
    return jsonify(data)


@bp.route('/categories/<int:id>/products', methods=['GET'])
def get_products_for_category(id:int):
    """
    Return products for  category
    """
    category = Category.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Category.to_collection_dict(category.products, page, per_page, 
                                    'api.get_products_for_category', id=id)
    return jsonify(data)