# print('Choose: \n1. Scan Face\n2. Register')
# choice = int(input('Your choice: '))

# # executing addRecord.py file if user chooses to register
# if choice==2:
# 	exec(open('addRecord.py').read())
# else:
# 	exec(open('viewRecord.py').read())


import pyrebase
# from flask import *
from flask import render_template, request, make_response, Flask
from flask_sqlalchemy import SQLAlchemy

#pyrebase Setup
config = {
	"apiKey": "AIzaSyBGjfeNaWOzjNiK40UaIH9F0YUny9TXfzQ",
    "authDomain": "facecan-db.firebaseapp.com",
    "databaseURL": "https://facecan-db.firebaseio.com",
    "projectId": "facecan-db",
    "storageBucket": "facecan-db.appspot.com",
    "messagingSenderId": "442953815031",
    "appId": "1:442953815031:web:ff3d72dd0e31be9981d4f2",
    "measurementId": "G-9QGMQF8LD8"
}


fireb = pyrebase.initialize_app(config)
auth = fireb.auth()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facedatadb.db'
db = SQLAlchemy(app)


class faces(db.Model):
	userId = db.Column(db.String, nullable=False)
	userName = db.Column(db.String(20), primary_key=True)
	name = db.Column(db.Text, default='N/A')
	upiId = db.Column(db.String, default='N/A')
	contactNumber = db.Column(db.Integer, default='N/A')
	emailId = db.Column(db.String, default='N/A')
	company = db.Column(db.String, default='N/A')
	address = db.Column(db.Text, default='N/A')
	fb_url = db.Column(db.Text, default='N/A')
	insta_handle = db.Column(db.String, default='N/A')
	twitter = db.Column(db.String, default='N/A')
	faceImage = db.Column(db.Boolean, default=False)
	emailVerified = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return 'faces ' + self.userName



# def setCookie(Email,CUI):
# 	cook = make_response('Setting Cookies')
# 	cook.set_cookie('Email', Email, max_age=60*60*24*365*2)
# 	cook.set_cookie('CUI', CUI, max_age=60*60*24*365*2)
# 	return cook


currentUserId = ''
faceImage = ''

@app.route('/')
def index():
	CuI = str(request.cookies.get('CUI'))
	Email = str(request.cookies.get('Email'))
	if (CuI == None or Email == None or Email == 'None' or CuI == 'None' or Email == '' or CuI == ''):
		return render_template('login.html')

	else:
		faceInfo = faces.query.filter_by(userId=CuI).first()
		
		if (faceInfo):
			return render_template('home.html', CUI=CuI, faceNotUpdated=False, Email=Email)
		else:
			return render_template('home.html', CUI=CuI, faceNotUpdated=True, Email=Email)
		




@app.route('/login', methods=['GET', 'POST'])
def basic():

	unsucc = 'Please check you credentials'
	CuI = str(request.cookies.get('CUI'))
	Email = str(request.cookies.get('Email'))

	if (CuI == None or Email == None or Email == 'None' or CuI == 'None' or Email == '' or CuI == ''):

		if request.method == 'POST':
			email = request.form['name']
			password = request.form['pass']

			#for logging user using pyrebase for firebase authentication
			try:
				user = auth.sign_in_with_email_and_password(email, password)
				global currentUserId
				currentUserId = user['localId']
			except:
				return render_template('login.html', us=unsucc)
			
			faceInfo = faces.query.filter_by(userId=str(currentUserId))

			#for checking if user is having username or not
			if faceInfo.count()>0:
				pass
			else:
				return render_template('addUserName.html', CUI=currentUserId, Email=email)

			#for sending user to homepage depending upon if his facedata is uploaded or not	
			faceInfo = faces.query.filter_by(userId=str(currentUserId)).first()
			global faceImage
			faceImage = faceInfo.faceImage
			if (faceImage):
				return render_template('home.html', CUI=currentUserId, faceNotUpdated=False, Email=email, UN=faceInfo.userName)
			else:
				return render_template('home.html', CUI=currentUserId, faceNotUpdated=True, Email=email, UN=faceInfo.userName)
				

	else:

		faceInfo = faces.query.filter_by(userId=CuI).first()

		if (faceInfo.faceImage):
				return render_template('home.html', CUI=CuI, faceNotUpdated=False, Email=Email, UN=faceInfo.userName)
		else:
			return render_template('home.html', CUI=CuI, faceNotUpdated=True, Email=Email, UN=faceInfo.userName)


	return render_template('login.html')





@app.route('/editprofile', methods=['GET', 'POST'])
def editprofile():

	CuI = str(request.cookies.get('CUI'))
	Email = str(request.cookies.get('Email'))

	if (CuI == None or Email == None or Email == 'None' or CuI == 'None' or Email == '' or CuI == ''):
		return render_template('login.html', msg='Login to continue...')

	if request.method == 'POST':
		f = faces.query.filter_by(userId=str(CuI)).first()
		f.userName = request.form['userName']
		f.name = request.form['name']
		f.upiId = request.form['upiId']
		f.contactNumber = request.form['contactNumber']
		f.emailId = request.form['emailId']
		f.company = request.form['company']
		f.address = request.form['address']
		f.fb_url = request.form['fb_url']
		f.insta_handle = request.form['insta_handle']
		f.twitter = request.form['twitter']
		db.session.commit()
		return render_template('viewProfile.html', face=f)
	faceInfo = faces.query.filter_by(userId= CuI).first()
	return render_template('editProfile.html', face=faceInfo)




@app.route('/viewprofile')
def viewprofile():

	CuI = str(request.cookies.get('CUI'))
	Email = str(request.cookies.get('Email'))

	if (CuI == None or Email == None or Email == 'None' or CuI == 'None' or Email == '' or CuI == ''):
		return render_template('login.html', msg='Login to continue...')

	faceInfo = faces.query.filter_by(userId= CuI).first()
	return render_template('viewProfile.html', face = faceInfo)





@app.route('/logout')
def logout():
	global currentUserId
	currentUserId = ''
	return render_template('logout.html')




@app.route('/signup', methods=['GET','POST'])
def signup():

	CuI = str(request.cookies.get('CUI'))
	Email = str(request.cookies.get('Email'))

	if (CuI == None or Email == None or Email == 'None' or CuI == 'None' or Email == '' or CuI == ''):
		unsucc = 'Signup failed! Please try again'
		if request.method == 'POST':
			email = request.form['name']
			password = request.form['pass']
			try:
				user = auth.create_user_with_email_and_password(email, password)
			except:
				return render_template('signup.html', us=unsucc)
			sucMsg = 'Account created successfully. Please login to continue..'
			return render_template('login.html', msg=sucMsg)

	else:
		faceInfo = faces.query.filter_by(userId=CuI).first()

		if (faceInfo):
				return render_template('home.html', CUI=currentUserId, faceNotUpdated=False, Email=Email, UN=faceInfo.userName)
		else:
			return render_template('home.html', CUI=currentUserId, faceNotUpdated=True, Email=Email, UN=faceInfo.userName)

	return render_template('signup.html')


@app.route('/addUserName', methods=['GET','POST'])
def addUserName():
	CuI = str(request.cookies.get('CUI'))
	Email = str(request.cookies.get('Email'))

	if (CuI == None or Email == None or Email == 'None' or CuI == 'None' or Email == '' or CuI == ''):
		return render_template('login.html', msg='Login to continue...')
	
	if request.method == 'POST':
		newUserName = request.form['userName']

		faceInfo = faces.query.filter_by(userName=newUserName)
		#for checking if username already exists
		if faceInfo.count()>0:
			return render_template('addUserName.html', msg='username already taken! try another', CUI=CuI, Email=Email)
		else:
			newRecord = faces(userId=CuI,userName=newUserName,emailId=Email)
			db.session.add(newRecord)
			db.session.commit()
			faceInfo = faces.query.filter_by(userId= CuI).first()
			if (faceImage):
				return render_template('home.html', CUI=CuI, faceNotUpdated=False, Email=Email, UN=faceInfo.userName)
			else:
				return render_template('home.html', CUI=CuI, faceNotUpdated=True, Email=Email, UN=faceInfo.userName)

	return render_template('home.html', CUI=CuI, faceNotUpdated=True, Email=Email)


@app.route('/scan')
def scanface():
	return '</h1>Scan face wali functionality add karega mai</h1>'

@app.route('/addface', methods=['GET','POST'])
def addface():
	if request.method=='POST':
		return 'Bahot achhe, wait karo, app under construction'
	return render_template('addface.html')

if __name__ == '__main__':
	app.run(debug=True)