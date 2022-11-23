# from app import db, init_db
from app.main import bp

@bp.before_app_first_request
def create_tables():
    """
    Prepopulate db
    """
    from app.init_db import dummy_data
    dummy_data()

@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    """
    Index page for site
    """
    return 'Hello World'
