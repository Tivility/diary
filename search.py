from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from diary.auth import login_required
from diary.db import get_db

bp = Blueprint('search', __name__)


@bp.route('/directory', methods=('GET', 'POST'))
@login_required
def directory():
    db = get_db()
    id = g.user['id']
    if id is None:
        return redirect('index')
    posts = db.execute(
        'SELECT DISTINCT dirname FROM post WHERE author_id = ?', (id,)
    ).fetchall()

    return render_template('search/directory.html', posts=posts)

@bp.route('/<dirname>/dirdetail', methods=('GET', 'POST'))
@login_required
def dirdetail(dirname):
    db = get_db()
    posts = db.execute(
        'SELECT id, title, body, created, author_id, tags'
        ' FROM post WHERE dirname = ? AND author_id = ?',
        (dirname, g.user['id'])
    ).fetchall()

    return render_template('search/dirdetail.html', 
            posts=posts, dirname=dirname)

@bp.route('/tags', methods=('GET', 'POST'))
@login_required
def tags():
    db = get_db()
    id = g.user['id']
    if id is None:
        return redirect('index')
    posts = db.execute(
        'SELECT DISTINCT name'
        ' FROM tag t JOIN post p ON t.post_id = p.id'
        ' WHERE p.author_id = ?', (g.user['id'],)
    ).fetchall()
    for post in posts:
        print("tag: ", post['name'])
    return render_template('search/tags.html', posts=posts)

@bp.route('/<name>/searchtag', methods=('GET', 'POST'))
@login_required
def searchtag(name):
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, tags'
        ' FROM post p JOIN tag t ON p.id = t.post_id'
        ' WHERE t.name = ?', (name,)
    ).fetchall()
    return render_template('search/searchtag.html', posts=posts, name=name)
