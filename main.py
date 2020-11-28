from flask import Flask, request, flash, url_for, redirect, render_template,session, abort
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:03lili24@localhost/facultad'
app.config['SECRET_KEY'] = "random string"


db = SQLAlchemy(app)


class Users (db.Model):
	id = db.Column('id', db.Integer(), primary_key = True)
	user_type = db.Column(db.Integer)
	dni = db.Column(db.Integer)
	firstname = db.Column(db.String(20))
	lastname = db.Column(db.String(20))
	email = db.Column (db.String(20))
	password = db.Column(db.String(50))
	 	


	def __init__(self, user_type, dni, firstname,lastname, email, password):

		self.user_type = user_type
		self.dni = dni
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.password = password

# esta es la tabla user_type q llena el combo. 

class User_type (db.Model):
	id = db.Column('id', db.Integer(), primary_key = True)
	description = db.Column (db.String(20))

	def __init__(self, description):

		self.description = description
		
			

@app.route('/show_users')
def show_users():
		
		return render_template('show_users.html', users = Users.query.all() )
		


@app.route('/new_user', methods = ['GET', 'POST'])
def new_user():
		if request.method == 'POST':
			   	  # chequea que no lleguen vacios los campos del nuevo user
			if  not request.form['user_type'] or not request.form ['dni'] or not request.form ['firstname'] or not request.form['lastname'] or not request.form['email']or not request.form['password']:
				flash('Please enter all the fields', 'error')
			else:
	      	 #se crea un objeto 
				user = Users( request.form['user_type'], request.form['dni'], request.form['firstname'], request.form['lastname'],
				request.form['email'], request.form['password'])
	         #aca se graba en la base datos 
				     
				db.session.add(user)

				db.session.commit()
	         
				flash('Record was successfully added')
				return redirect(url_for('show_users'))

		return render_template('new_user.html',users_type = User_type.query.all())
	



if __name__ == '__main__':
   app.run(debug=True)
	
	   


