from flask import render_template, request, redirect, flash, url_for
from app import app
from app.forms import LoginForm
import datetime

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Elinor'}
	posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
	return render_template('index.html', title="corndog", user=user, posts=posts)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    user = {'username': 'Elinor'}
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me{}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template(url_for('schedule'), title='Sign In', user=user, form=form)