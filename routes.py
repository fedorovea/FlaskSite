from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    send_from_directory,
    request,
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)
from werkzeug.routing import BuildError

from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from app import create_app, db, login_manager, bcrypt
from models import User, itemDB
from forms import login_form, register_form


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app = create_app()


@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
    return render_template("index.html", title="Home")


@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()

    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('about'))
            else:
                flash("Неправильное имя пользователя или пароль!", "Опасность")
        except Exception as e:
            flash(e, "Опасность")

    return render_template("personal_area.html",
                           form=form,
                           text='',
                           title="Login",
                           btn_action="Войти"
                           )


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)


# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            email = form.email.data
            pwd = form.pwd.data
            username = form.username.data

            newuser = User(
                username=username,
                email=email,
                pwd=bcrypt.generate_password_hash(pwd),
            )

            db.session.add(newuser)
            db.session.commit()
            flash(f"Аккаунт успешно создан", "Успех!")
            return redirect(url_for("login"))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Что-то пошло не так!", "Опасность")
        except IntegrityError:
            db.session.rollback()
            flash(f"Пользователь уже существует", "Предупрежедние")
        except DataError:
            db.session.rollback()
            flash(f"Неверные данные", "Предупрежедние")
        except InterfaceError:
            db.session.rollback()
            flash(f"Ошибка подключения к базе данных", "Опасность")
        except DatabaseError:
            db.session.rollback()
            flash(f"Ошибка подключения к базе данных", "Опасность")
        except BuildError:
            db.session.rollback()
            flash(f"Произошла ошибка!", "Опасность")
    return render_template("personal_area.html",
                           form=form,
                           text="",
                           title="Register",
                           btn_action="Зарегистрировать аккаунт"
                           )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/user_suggestions')
@login_required
def user_suggestions():
    items = itemDB.query.order_by(itemDB.price).all()
    return render_template('user_suggestions.html', sug=items)


@app.route('/create/', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        description = request.form['description']

        item = itemDB(title=title, price=price, description=description)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/user_suggestions')
        except:
            return "ERORORR"
    else:
        return render_template('create.html')


@app.route('/error', methods=['GET'])
def error():
    return render_template('/error.html'), {"Refresh": "10; url=https://mdc.mo.gov/hunting-trapping/species/deer"}


if __name__ == "__main__":
    app.run(debug=False)