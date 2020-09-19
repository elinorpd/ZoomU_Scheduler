from my_app import app

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Elinor'}
	return render_template('index.html', title="Title", user=user)