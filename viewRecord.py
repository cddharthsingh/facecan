# importing libraries
import cv2
import face_recognition as fr
import pickle
from firebase import firebase

# firebase authentication URL
firebase = firebase.FirebaseApplication("https://facecan-db.firebaseio.com/", None)

print('Scanning the face....')
# loading data from .pickle file
data = pickle.loads(open("encodings.pickle", "rb").read())
encodingsBox = data["encodings"]
userkeyBox = data["names"]

# loading image from folder and creating face encodings
new_image = fr.load_image_file('./img/known/siddharth.jpg')
new_image_encoding = fr.face_encodings(new_image)[0]	

# checking if new face encode exists in data
counter = 0
userNotFound = True
for i in encodingsBox:
	if not((new_image_encoding - i).all()): #comparing arrays
		username = userkeyBox[counter]
		url = '/users/'+ username
		result = firebase.get(url, None)
		for j in result:
			print('----------------------------------')
			print('|  ', j,' | ',result[j], '  | ')
		print('----------------------------------')
		userNotFound = False
		break
	else: counter += 1

if (userNotFound):
	print('Sorry!! User is not registered.')

print('Go back to homepage? y/n : ')
if (input('choice: '))=='y':
	exec(open('app.py').read())
else: print('Bye!!')