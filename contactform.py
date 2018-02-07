from flask import Flask, render_template, request, flash
from forms import ContactForm
from flask_pymongo import PyMongo
 
app = Flask(__name__)
mongo = PyMongo('test')

app.secret_key = 'development key'

@app.route('/contact', methods = ['GET', 'POST'])
def contact():
	users = mongo.db.users.find({})
	for user in users:
		print repr(user.username), repr(user.email)
	form = ContactForm()
	if request.method == 'GET':
		return render_template('contact.html', form = form)
	if request.method == 'POST':
		if form.validate() == False:
			flash('All fields are required.')
			return render_template('contact.html', form = form)
		else:
			return render_template('hello.html')


if __name__ == '__main__':
   app.run(debug = True)
