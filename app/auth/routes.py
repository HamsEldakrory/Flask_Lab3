from flask import Blueprint
from  flask import render_template,redirect,url_for,flash,request
from app.models import User
from app.auth.forms import registerForm,loginForm
from flask_login import login_user,logout_user,login_required
auth_blueprint = Blueprint('auth', __name__,url_prefix='/auth')

@auth_blueprint.route('/register',methods=['GET','POST'])
def register():
    form = registerForm()
    if form.validate_on_submit():
        user=User(email=form.email.data,first_name=form.first_name.data,last_name=form.last_name.data,password=form.password.data)
        user.save_to_db()
        return redirect(url_for('main.book_list'))
    return render_template('auth/register.html',form=form)

@auth_blueprint.route('/login',methods=['GET','POST'],endpoint='login')
def login():
    form=loginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            next_page=request.args.get('next')
            if not next_page:
                return redirect(url_for('main.book_list'))
            return redirect(next_page)
        flash('Invalid email or password.')
    return render_template('auth/login.html',form=form)
@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))