from flask import render_template, request, redirect, flash, url_for
from app import app
from app.forms import LoginForm
import datetime

@app.route('/')
@app.route('/index')
def index():
    #print("hello world")
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
    name = request.form['gcal']
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me{}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('schedule.html', title='Sign In', user=user, form=form, gcal=name)