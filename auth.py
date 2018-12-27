import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from diary.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        headimge = "default.jpg"
        db = get_db()
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id'
                ' FROM user'
                ' WHERE username = ?', (username,) 
            ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, headimge) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), headimge)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        db.commit()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

#       if request.form['username'] == '0':
#       error = None

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        print("error: ", error)

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    print("id = ", id)
    db = get_db()
    post = db.execute(
        'SELECT username, password'
        ' FROM user'
        ' WHERE id = ?', (id,)
    ).fetchone()
    db.commit()
    if (request.method == 'POST'):
        username = request.form['username']
        used = False
        check = db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchall()
        for row in check:
            for item in row:
                if (item != id):
                    used = True
        password = request.form['password']
        error    = None

        if not username:
            error = "username is required"
        if not password:
            error = "password is required"
        if used:
            error = "username is used by others"

        if error is not None:
            flash(error)
        else :
            print("username = ", username)
            print("psw = ", password)
            db.execute(
                'UPDATE user'
                ' SET username = ?, password = ?'
                ' WHERE id = ?', (username, generate_password_hash(password), id)
            )
            db.commit()
            return redirect(url_for('diarybook.index'))
    return render_template('auth/update.html', post=post)


'''
TODO: user head img
@bp.route('/updimg/<int:id>', methods=('GET', 'POST'))
@login_required
def updimg(id):
    db = get_db()
    post = db.execute(
        'SELECT headimge FROM user WHERE id = ?', (id,)
    ).fetchone()
    db.commit()
    if (request.method == 'POST'):
        file = request.files['file']
        file.save("./".id."jpg")
        db.execute(
            'UPDATE user SET headimge = ? WHERE id = ?', 
            (id."jpg", id)
        )
        db.commit()
        return redirect(url_for('diarybook.index'))
    return render_template('auth/updimg.html', post=post)
'''

