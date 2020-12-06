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
	nationality = db.Column(db.Integer)
	gender = db.Column(db.Integer)
	 	


	def __init__(self, user_type, dni, firstname,lastname, email, password, nationality, gender):

		self.user_type = user_type
		self.dni = dni
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.password = password
		self.nationality = nationality
		self.gender = gender

# esta es la tabla user_type q llena el combo. 

class User_type (db.Model):
	id = db.Column('id', db.Integer(), primary_key = True)
	description = db.Column (db.String(20))

	def __init__(self, description):

		self.description = description


class Nationality (db.Model):
	id = db.Column('id', db.Integer(), primary_key = True)
	description = db.Column (db.String(20))

	def __init__(self, description):

		self.description = description
		
class Gender (db.Model):
	id = db.Column('id', db.Integer(), primary_key = True)
	description = db.Column (db.String(20))

	def __init__(self, description):

		self.description = description		

@app.route('/show_users')
def show_users():
		
		
		return render_template('show_users.html',users = Users.query
			.join(Nationality, Users.nationality==Nationality.id)
			.join(Gender, Users.gender==Gender.id)
			.add_columns(Users.id,
					 	Users.user_type, 
						Users.email, 
						Users.dni,
					 	Users.firstname, 
						Users.lastname, 
						Users.password,
					 	Nationality.description,
					 	Gender.description.label("genero")  ) )

@app.route('/new_user', methods = ['GET', 'POST'])
def new_user():
		if request.method == 'POST':
			   	  # chequea que no lleguen vacios los campos del nuevo user
			if  not request.form['user_type'] or not request.form ['dni'] or not request.form ['firstname'] or not request.form['lastname'] or not request.form['email']or not request.form['password'] or not request.form['nationality'] or not request.form['gender']:
				flash('Please enter all the fields', 'error')
			else:
	      	 #se crea un objeto 
				user = Users( request.form['user_type'], request.form['dni'], request.form['firstname'], request.form['lastname'],
				request.form['email'], request.form['password'], request.form['nationality'], request.form['gender'])
	         #aca se graba en la base datos 
				     
				db.session.add(user)

				db.session.commit()
				
	         
				flash('Record was successfully added')
				return redirect(url_for('show_users'))

		return render_template('new_user.html',users_type = User_type.query.all(), nationality = Nationality.query.all(), gender = Gender.query.all() )
	

@app.route('/delete/<int:id>')
def delete(id):
		user = Users.query.filter_by(id=id).first()
		
		if user is not None:
		 user = Users.query.get(id)
		 db.session.delete(user)
		 db.session.commit()
		 flash ('borro el usuario:')
		 flash (user.firstname)
		 return render_template('show_users.html',users = Users.query
			.join(Nationality, Users.nationality==Nationality.id)
			.join(Gender, Users.gender==Gender.id)
			.add_columns(Users.id,
					 	Users.user_type, 
						Users.email, 
						Users.dni,
					 	Users.firstname, 
						Users.lastname, 
						Users.password,
					 	Nationality.description,
					 	Gender.description.label("genero")  ) )
		else:
		 flash('No existe ese id', 'error')		
		 return redirect(url_for('show_users'))


@app.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
	
		
		#cuando entra por POST
		if request.method == 'POST':
			#aca recupera de la tabla el usuario con ese id de la base de datos
			user = Users.query.filter_by(id=request.form['id']).first()

	   	  # chequea que no lleguen vacios los campos 
			if not request.form['user_type'] or not request.form['dni']or not request.form['firstname']or not request.form['lastname'] or not request.form['password'] or not request.form['nationality']or not request.form['gender']:
				flash('Please enter all the fields', 'error')
				user = Users.query.filter_by(id=id).first()
				return render_template('edit.html', users= user ,  nationality = Nationality.query.all(),gender = Gender.query.all())
				
			else:
	      	 #se actualza un objeto estudiante  de la clase students
				user.user_type = request.form['user_type']
				user.dni = request.form['dni']
				user.firstname = request.form['firstname']
				user.lastname = request.form['lastname']
				user.password = request.form['password'] 
				user.nationality = request.form['nationality'] 
				user.gender = request.form['gender']
	         #aca se actualiza 
				
				db.session.commit()
	         
				flash('Record was successfully added')
				return redirect(url_for('show_users'))
		#esto hace cuando viene del GET		
		#cuando entra por GET hace :
		else:

			user = Users.query.filter_by(id=id).first()
			return render_template('edit.html', users = user , nationality = Nationality.query.all(),gender = Gender.query.all())	

	
		    

	
		    

if __name__ == '__main__':
   app.run(debug=True)
	
	   


