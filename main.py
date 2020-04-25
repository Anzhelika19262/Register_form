from flask import Flask
from data import db_session, users
from register import RegisterForm
from flask import render_template, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/users.sqlite")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register Form',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Register Form',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return jsonify({'status': 'ok'})
    return render_template('register.html', title='Register Form', form=form)


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
