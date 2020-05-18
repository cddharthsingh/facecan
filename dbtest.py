from firebase import firebase


firebase = firebase.FirebaseApplication("https://facecan-db.firebaseio.com/", None)
data = {
	'Name': 'Siddharth Singh',
	'Email': 'cddharthsingh.com',
	'Phone': 8423790364
}
lol = 'sid'
result = firebase.delete('/users/+lol+/','')
print(result)