from app.main import bp


@bp.route('/', methods=['GET'])
@bp.route('/index', methods=['GET'])
def index():
    """
    Index page for site
    """
    return 'Hello World'
