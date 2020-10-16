from flask import Flask, render_template, flash, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'bhavik'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web.db'
login_manager = LoginManager(app)
from forms import RegisterForm, LoginForm
from models import db, User

db.init_app(app)
bcrypt = Bcrypt(app)

posts = [{'title': f'Post {i}', 'description': f'description {i}',
          'image': f'static/{i}.jpg' if i != 0 and 5 > i else f'static/{5}.jpg'} for i in range(0, 50)]


@app.route('/')
def home():
    return render_template("index.html", posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(password=form.password.data).decode('utf-8')
        user = User(enrollment=form.enrollment.data, email=form.email.data, password=hash_password,
                    first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(enrollment=form.enrollment.data).first()
        if user and bcrypt.check_password_hash(password=form.password.data, pw_hash=user.password):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, Please check enrollment and password!', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
