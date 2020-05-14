# importing libraries
import cv2
import face_recognition as fr
import pickle
from firebase import firebase

# firebase authentication URL
firebase = firebase.FirebaseApplication("https://facecan-db.firebaseio.com/", None)

# loading data from .pickle file
data = pickle.loads(open("encodings.pickle", "rb").read())
encodingsBox = data["encodings"]
userkeyBox = data["names"]

# loading data for the first time - above three lines should be commented before using following two lines.
# encodingsBox = []
# userkeyBox = []


# capturing image from webcam using open cv2
#number of frames to throw away while the camera adjusts to light
# ramp_frames = 30
# # initializing camera with port 0 (default for webcam)
# camera = cv2.VideoCapture(-1)
# # captures a single image from the camera and returns it in PIL format
# def get_image():
# 	retval, im = camera.read()
# 	return im
# # following code will let camera adjust by discarding photos
# for i in range(ramp_frames):
# 	temp = get_image()
# print("Wait.. taking image...")
# camera_capture = get_image()
# # file = './img/clicks/test.png'
# # saving image
# cv2.imwrite('test.png', camera_capture)
# del(camera)



# loading image from folder and creating face encodings
new_image = fr.load_image_file('./img/known/siddharth.jpg')
new_image_encoding = fr.face_encodings(new_image)[0]

counter = 0
notFound = True

# checking if new face encode exists in data
for i in encodingsBox:
	if not((new_image_encoding - i).all()): #comparing arrays
		notFound = False
		break;
	counter += 1

# if does not exists
if(notFound):
	encodingsBox.append(new_image_encoding)
	usernameNotFound = True
	while(usernameNotFound): #finding unique username
		userkey = input('Enter UserName: ')
		if userkey not in userkeyBox:
			userkeyBox.append(userkey)
			usernameNotFound = False
		else:
			print('Username already exists. Enter something else: ')

	# getting data to store in firebase
	name = input('Enter name: ')
	phone = input('Enter phone number: ')
	upiID = input('Enter your UPI ID for ex(name@sbi): ')
	fb = input('Enter Facebook username (type none if N/a): ')
	insta = input('Enter Instagram username (type none if N/a): ')
	email = input('Enter E-mail ID: ')

	url = '/users/' + userkey

	#firebase data packet
	fb_data = {
		'Name' : name,
		'Phone' : phone,
		'upiID' : upiID,
		'fb'	: fb,
		'insta' : insta,
		'email' : email
	}

	result = firebase.patch(url,fb_data)
	print(result, '\nRecord added succesfully!')

else:
	print('User already registered by username ' + userkeyBox[counter])
	

data = {"encodings": encodingsBox, "names": userkeyBox}
f = open("encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()

print('Go back to homepage? y/n : ')
if (input('choice: '))=='y':
	exec(open('app.py').read())
else: print('Bye!!')
