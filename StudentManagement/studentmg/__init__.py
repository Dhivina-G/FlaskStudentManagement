import os
from flask import Flask,url_for
from studentmg import db


def create_app(test_config = None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'stdmgt',
        DATABASE = os.path.join(app.instance_path,'studmg.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    from . import db
    db.init_app(app)

    from . import studm
    app.register_blueprint(studm.bp)

    return app

    