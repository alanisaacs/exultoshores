from flask import Blueprint

labels_bp = Blueprint(
    'labels_bp', __name__,
    static_folder='static',
    static_url_path='/labels/static'
    )
