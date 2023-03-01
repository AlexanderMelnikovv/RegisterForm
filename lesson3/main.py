from flask import Flask, render_template
from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "yandexlyceum_secret_key"


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    db_session.global_init('db/reg_user.db')
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message='Такой пользователь уже есть!')

        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            address=form.address.data,
            speciality=form.speciality.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
    return render_template('register.html', title='Регистрация', form=form)


def main():
    '''name = input()
    global_init(name)
    db_sess = create_session()
    first_module = db_sess.query(Jobs).filter(Jobs.collaborators == 1).first:
    print(first_module)'''
    '''db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == 2)         # | - or    , - and
    user.delete()
    db_sess.commit()
    news = News(title='Конкурс строя и песни', content='Завтра рег по технологии',
                user_id=1, is_private=False)
    db_sess.add(news)
    db_sess.commit()
    user = User()
    user.name = 'Lodyr1'
    user.about = 'Bezdelnikov'
    user.email = 'email@mail.ru'
    db_sess = db_session.create_session()
    db_sess.add(user)
    user2 = User(name='Ilya', about='Lodyr', email='Bikmev@yandex.ru')
    db_sess.add(user2)
    db_sess.commit()'''
    app.run()


if __name__ == "__main__":
    main()