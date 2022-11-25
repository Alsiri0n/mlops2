from flask import jsonify, request
from app import db
from app.api import bp
from app.models import Product, Category


@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id:int):
    """
    Return product by id
    """
    return jsonify(db.get_or_404(Product, id).to_dict('api.get_product', False))


@bp.route('/products', methods=['GET'])
def get_products():
    """
    Return all products
    """
    data = Product.full_dict(query=db.select(Product), endpoint='api.get_products')
    return jsonify(data)


@bp.route('/products/all', methods=['GET'])
def get_products_all():
    """
    Return products and categories
    """
    data = Product.full_dict(
        db.select(Product, Category).join(Product.categories, isouter=True), 'api.get_product_all')
    return jsonify(data)


@bp.route('/products/<int:id>/categories', methods=['GET'])
def get_categories_for_product(id:int):
    """
    Return categories for product
    """
    product = db.get_or_404(Product, id)
    data = Product.full_dict(product.categories,'api.get_categories_for_product', id=id)
    return jsonify(data)


@bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id:int):
    """
    Return category by id
    """
    return jsonify(db.get_or_404(Category, id).to_dict('api.get_category', False))


@bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Return all categories
    """
    data = Category.full_dict(query=db.select(Category), endpoint='api.get_categories')
    return jsonify(data)


@bp.route('/categories/all', methods=['GET'])
def get_categoriess_all():
    """
    Return all categories with products
    """
    data = Category.full_dict(
        db.select(Category, Product).join(Product.categories, full=True), 'api.get_categories_all')
    return jsonify(data)


@bp.route('/categories/<int:id>/products', methods=['GET'])
def get_products_for_category(id:int):
    """
    Return products for  category
    """
    category = db.get_or_404(Category, id)
    data = Category.full_dict(category.products, 'api.get_products_for_category', id=id)
    return jsonify(data)


@bp.route('/alldata', methods=['GET'])
def get_alldata():
    """
    Return all data
    """
    # category = db.get_or_404(Category, id)
    data = Product.all_data()
    return jsonify(data)