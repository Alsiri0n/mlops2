from flask import jsonify, request
from app import db
from app.api import bp
from app.models import Product, Category


@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id:int):
    """
    Return product by id
    """
    return jsonify(db.get_or_404(Product, id).to_dict())


@bp.route('/products', methods=['GET'])
def get_products():
    """
    Return all products
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Product.to_collection_dict(db.select(Product), page, per_page, 'api.get_products')
    return jsonify(data)


@bp.route('/products/all', methods=['GET'])
def get_productsall():
    """
    Return products and categories
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Product.to_collection_dict(
        db.select(Product, Category).\
        join(Product.categories, isouter=True),
         page, per_page, 'api.get_productsall', True)
    
    return jsonify(data)


@bp.route('/products/<int:id>/categories', methods=['GET'])
def get_categories_for_product(id:int):
    """
    Return categories for product
    """
    # product = Product.query.get_or_404(id)
    product = db.get_or_404(Product, id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Product.to_collection_dict(product.categories, page, per_page,
                                    'api.get_categories_for_product', id=id)
    return jsonify(data)


@bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id:int):
    """
    Return category by id
    """
    return jsonify(db.get_or_404(Category, id).to_dict())

@bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Return all categories
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Category.to_collection_dict(db.select(Category), page, per_page, 'api.get_categories')
    return jsonify(data)


@bp.route('/categories/<int:id>/products', methods=['GET'])
def get_products_for_category(id:int):
    """
    Return products for  category
    """
    category = db.get_or_404(Category, id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Category.to_collection_dict(category.products, page, per_page, 
                                    'api.get_products_for_category', id=id)
    return jsonify(data)