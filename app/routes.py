from flask import render_template, request, redirect
from app import app
from app.forms import LoginForm

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

@app.route('/login')
def login():
    user = {'username': 'Elinor'}
    form = LoginForm()
    return render_template('login.html', title='Sign In', user=user, form=form)