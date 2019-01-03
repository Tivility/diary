import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from flask_wtf import FlaskForm

from diary.auth import login_required
from diary.db import get_db

bp = Blueprint('test', __name__, url_prefix='/test')


class PostForm(FlaskForm):
    title = 'Title'
    text = 'Content'
    categories = 1

    def __init__(self):
        super(PostForm, self).__init__()
        #self.categories.choices = [(c.id, c.title) for c in Category.query.order_by('id')]


@bp.route('/test', methods=('GET', 'POST'))
def test():
    print("now start test")
    return render_template('test/test.html')
    

@bp.route('/testedit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    form = PostForm()
    
    form.title = "welcome"
    form.text = '''
        # header
        ## header2
        * 1
        * 2
        * 3
        **blod**
    '''
    return render_template('test/edit.html', form=form)
    
@bp.route('/testshow', methods=('GET', 'POST'))
def testshow():
    mkd = '''
        # header
        ## header2
        * 1
        * 2
        * 3
        **blod**
    '''
    return render_template('test/testshow.html', mkd=mkd)
