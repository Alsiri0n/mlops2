from app.init_db import clear_data, dummy_data
from app.main import bp
from flask import render_template, request, flash

# @bp.before_app_first_request
# def create_tables():
#     """
#     Prepopulate db
#     """
#     from app.init_db import dummy_data
#     dummy_data()

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """
    Index page for site
    """
    if request.method == 'POST':
        if 'reset' in request.form:
            clear_data()
            flash('Data cleared')
        if 'populate' in request.form:
            dummy_data()
            flash('Data populated')
    return render_template('base.html')
