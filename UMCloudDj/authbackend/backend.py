# import the User object
from django.contrib.auth.models import User
from django.contrib import auth
import xmlrpclib as xmlrpc 	#Used for authenticating against wordpress using xmlrpc client

# Name my backend 'MyCustomBackend'
class MyCustomBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure

    def authenticate(self, username=None, password=None):

        try:
            # Try to find a user matching your username
            user = User.objects.get(username=username)
	    
	    #Check username and password here..
            #  Check the password is the reverse of the username
            if password == username[::-1]:
                # Yes? return the Django user object
		print("Username and Password check success")
                return user
            else:
                # No? return None - triggers default login failed
		print("Username and Password check unsuccessfull")
                return None

        except User.DoesNotExist:
            # No user was found, return None - triggers default login failed
	    print("User Does Not Exists")

	    #Check user credentials

	    s = xmlrpc.ServerProxy('http://www.ustadmobile.com/xmlrpc.php')	#Getting the xmlrpc link for ustadmobile.com wordpress
	    if s.wpse39662.login(username,password):				#Returns true if user is successfully authenticated, False if not
	    	print("Username and Password check success for new user.")
		print("Checking new user in Django..")
		#Create user.
		user_count = User.objects.filter(username=username).count()
        	if user_count == 0:
			print ("User doesn't exist, creating user..")
			user = User(username=username, email=username)
    			user.set_password(password)
    			user.save()
			print("User created!")
        		#return auth_and_login(request)
			return user;
    		else:
        		#Show message that the username/email address already exists in our database.
			print("Error in creating user. User already exists!")
        		return redirect("/login/")

	    else:
		print("Username and Password check unsuccessfull for new user. Not creating new user.")
		return None

            #return None

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
	print("In get_user")
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
	    print("User does not exist")
            return None
