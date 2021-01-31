from app import app, db, login_manager
from flask_login import login_user, login_required, current_user, logout_user

from .models import Users, Events
from .userlogin import UserLogin
from .forms import LoginForm, RegistrationForm, CreateEventsForm

from flask import render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import MultiDict


# Формирует экземпляр класса UserLogin при каждом запросе от сайта
# функция вызывается если в сессии есть информация _id юзера от login_user
@login_manager.user_loader
def load_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    return UserLogin(user=user)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/authorization', methods=["POST", "GET"])
def authorization():
    if current_user.is_authenticated:
        return redirect('profile')

    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.psw, form.psw.data):
            # Создаём экземпляр текущего пользователя передавая объект юзера из БД
            user_login = UserLogin(user=user)
            rm = form.remember_me.data
            # заносим в сессию информацию о текущем пользователе
            login_user(user_login, remember=rm)
            # Через переменную next получаем путь к странице с которой отправили пользователя авторизоваться
            return redirect(request.args.get('next') or url_for('profile'))
        flash('Wrong email or password.', 'danger')
    return render_template("authorization.html", form=form)


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            psw_hash = generate_password_hash(form.psw.data)
            res = Users(
                username=form.username.data,
                email=form.email.data,
                psw=psw_hash,
            )
            db.session.add(res)
            db.session.commit()
            flash("Registration success.", 'success')
            return redirect(url_for('authorization'))
        except:
            db.session.rollback()
            flash("Mistake in db.", 'danger')

    return render_template('registration.html', form=form)


@app.route('/events')
@login_required
def events():
    events_list = Events.query.all()
    return render_template('events.html', events=events_list)


# Удаляет из сессии информацию id о юзере и его сессии, которую туда записала функция login_user
# и теперь @login_manager.user_loader вызываться не будет, т.е. не будет создаваться экземпляр
# текущего пользователя
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "success")
    return redirect('authorization')


@app.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated:
        # current_user - глобальная переменная доступная как в маршутах, так и в шаблонах
        # доступны прописанные в UserLogin методы get_id и get_name
        user = Users.query.filter_by(id=current_user.get_id()).first()
        form = RegistrationForm(MultiDict([('username', user.username),
                                           ('email', user.email),
                                           ('date', user.date.strftime("%A, %d. %B %Y %I:%M%p"))]))
        return render_template('profile.html', form=form, user=user)


@app.route('/createevent', methods=['POST', 'GET'])
@login_required
def create_event():
    if current_user.is_authenticated:
        form = CreateEventsForm()
        if form.validate_on_submit():
            try:
                event = Events(
                    author=current_user.get_name(),
                    begin=form.begin.data,
                    end=form.end.data,
                    topic=form.topic.data,
                    description=form.description.data
                )
                db.session.add(event)
                db.session.commit()
                flash("Registration success.", 'success')
                return redirect(url_for('events'))
            except:
                db.session.rollback()
                flash("Mistake in db.", 'danger')
        return render_template('createevent.html', form=form)


@app.route('/changeevent', methods=['POST', 'GET'])
@login_required
def changeevent():
    if current_user.is_authenticated:
        if request.method == "POST":
            form = CreateEventsForm()
            if form.validate_on_submit():
                try:
                    Events.query.filter_by(_id=request.args.get('event_id')).update(dict(
                        begin=form.begin.data,
                        end=form.end.data,
                        topic=form.topic.data,
                        description=form.description.data))
                    db.session.commit()
                    flash("Change success.", 'success')
                    return redirect(url_for('events'))
                except:
                    db.session.rollback()
                    flash("Mistake in db.", 'danger')
            return render_template('changeevent.html', form=form)
        event = Events.query.filter_by(_id=request.args.get('event_id')).first()
        form_event = CreateEventsForm(MultiDict([('begin', str(event.begin)),
                                           ('end', str(event.end)),
                                           ('topic', event.topic),
                                           ('description', event.description)]))
        return render_template('changeevent.html', form=form_event)


@app.route('/deleteevent')
@login_required
def deleteevent():
    if current_user.is_authenticated:
        try:
            event = Events.query.filter_by(_id=request.args.get('event_id')).first()
            db.session.delete(event)
            db.session.commit()
            flash("Deleting success.", 'success')
            return redirect(url_for('events'))
        except:
            db.session.rollback()
            flash("Mistake in db.", 'danger')
    return redirect(url_for('events'))
