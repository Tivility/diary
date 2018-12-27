from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from diary.auth import login_required
from diary.db import get_db

bp = Blueprint('diarybook', __name__)


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, dirname, tags'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (id,)
    ).fetchone()
    if (post is None):
        abort(404, "Post id {0} dosn't exist.".format(id))

    if (check_author and post['author_id'] != g.user['id']):
        abort(403)

    return post

@bp.route('/')
def index():
    db = get_db()
    if (g.user):
        posts = db.execute(
            'SELECT p.id, title, body, created, author_id, username'
            ' FROM post p JOIN user u ON p.author_id = u.id'
            ' WHERE u.id = ? AND dirname != "trash"'
            ' ORDER BY created DESC', (g.user['id'], )
        ).fetchall()
    else :
    # Todo: add an welcome post and show welcome to register
        posts = db.execute(
            'SELECT id, title, body, created, author_id'
            ' FROM post'
            ' WHERE author_id = 0'
        ).fetchall()
    print("show posts")
    for post in posts:
        for item in post:
            print(item)
    print("show posts end")
    return render_template('diarybook/index.html', posts=posts)

@bp.route('/<int:id>', methods=('GET', 'POST'))
@bp.route('/<int:id>/detail', methods=('GET', 'POST'))
@login_required
def detail(id):
    db = get_db()
    post = db.execute(
        'SELECT id, title, body, created, author_id, dirname'
        ' FROM post'
        ' WHERE id = ?', (id,)
    ).fetchone()
    tags = db.execute(
        'SELECT name FROM tag WHERE post_id = ?', (id,)
    ).fetchall()
    if (tags):
        print("show tags:")
        for item in tags:
            print(item['name'])
    if (post):
        for item in post:
            print(type(item), item)
        if (post[4] != g.user['id']):
            return redirect(url_for('diarybook.index'))
        return render_template('diarybook/detail.html', post = post, tags = tags)

    return redirect(url_for('diarybook.index'))

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if (request.method == 'POST'):
        title = request.form['title']
        body = request.form['body']
        dirname = request.form['dirname']
        print(dirname)
        tags = request.form['tags']
        error = None
        if not title:
            error = 'Title is required.'
        if dirname == "trash":
            error = 'dirname is not allow use "trash"'
        if not dirname:
            dirname = "auto"
        if error is not None:
            flash(error)
        else :
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, dirname, tags)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, g.user['id'], dirname.lower(), tags.lower())
            )
            db.commit()
            post_id = db.execute(
                'SELECT last_insert_rowid() newid'
            ).fetchone()[0]
            print("post_id:", post_id)
            taglist = set(tags.lower().replace(", ", ",").split(","))
            for tag in taglist:
                print ("tag: ", tag)
                db.execute(
                    'INSERT INTO tag (post_id, name)'
                    ' VALUES (?, ?)',
                    (post_id, tag)
                )
                db.commit()
            return redirect(url_for('diarybook.index'))

    return render_template('diarybook/create.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if (request.method == 'POST'):
        title   = request.form['title']
        body    = request.form['body']
        dirname = request.form['dirname']
        tags    = request.form['tags']
        error   = None

        print("show request.form")
        for item in request.form:
            print(item)
        print("show request.form end")

        if not title:
            error = "Title is required"
        if dirname == "trash":
            error = 'dirname is not allow use "trash"'

        if error is not None:
            flash(error)
        
        else :
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?, dirname = ?, tags = ?'
                ' WHERE id = ?', (title, body, dirname.lower(), tags.lower(), id)
            )
            db.commit()
            db.execute('DELETE FROM tag WHERE post_id = ?', (id,))
            db.commit()
            taglist = set(tags.lower().replace(", ", ",").split(","))
            for tag in taglist:
                print ("tag: ", tag)
                db.execute(
                    'INSERT INTO tag (post_id, name)'
                    ' VALUES (?, ?)',
                    (id, tag)
                )
                db.commit()
            return redirect(url_for('diarybook.index'))

    return render_template('diarybook/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM tag WHERE post_id = ?', (id,))
    db.commit()
    db.execute(
        'UPDATE post'
        ' SET dirname = "trash"'
        ' WHERE id = ?', (id,)
    )
    db.commit()
    return redirect(url_for('diarybook.index'))

