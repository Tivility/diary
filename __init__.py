import os
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    from flaskext.markdown import Markdown

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'diary.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exits, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    #ensure the instance folder exits
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

    
    from diary import db
    db.init_app(app)

    from diary import auth
    app.register_blueprint(auth.bp)

    from diary import diarybook
    app.register_blueprint(diarybook.bp)
    app.add_url_rule('/', endpoint='index')
    
    from diary import search
    app.register_blueprint(search.bp)     

    from diary import test
    app.register_blueprint(test.bp)

    Markdown(app)
    
    return app
