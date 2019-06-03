from . import profile
from flask_login import login_required


@profile.route('/')
@login_required
def index():
    return 'Profile'
