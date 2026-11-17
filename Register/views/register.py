from django.shortcuts import render, redirect
from django.views import View
# Importing django hasher to hash the user entered passowrd
from django.contrib.auth.hashers import make_password
# Importing Staff and User model to fetch objects and verify user entered data
from Register.models import Staff, User
# Importing the authentication package for validating the JWT token if there is any in the session
from Register.jwt.validate import validate
# Importing random to generate a randomized string for unique user ID
import random
# Importing string to generate strings that are randomized by the random module for unique user ID
import string


class register(View):
    def get(self, request):

        # Checking token in session
        if request.session.get('token'):
            token = request.session.get('token')
            validation = validate(token)
            tokenCheck = validation.get('status')

            # Token validation and redirection to homepage upon success
            if tokenCheck:
                return redirect('homepage')
            
            # Deleting token from session after unsuccessful verification
            del request.session['token']

        return render(request, 'register.html')


    def post(self, request):

        # Checking token in session
        if request.session.get('token'):
            token = request.session.get('token')
            validation = validate(token)
            tokenCheck = validation.get('status')

            # Token validation and redirection to homepage upon success
            if tokenCheck:
                return redirect('homepage')
            
            # Deleting token from session after unsuccessful validation
            del request.session['token']


        # Getting register form data after unsuccussful token check or validation
        formData = request.POST
        csid = formData.get('csid')
        email = formData.get('email')
        password = formData.get('password')
        repassword = formData.get('repassword')

        # Passing Staff ID and Email entered by the user in a dictionary so they can be sent to the frontend to be autofilled in case of any errors.
        value = {
            'csid' : csid,
            'email' : email,
        }

        # Getting a staff object with user entered Staff ID for form data validation
        staffID = Staff.get_staff_by_csid(csid)

        # Getting a staff object with user entered Email for form data validation
        staffemail = Staff.get_staff_by_email(email)

        # Getting a user object with user entered Email for form data validation
        userCheck = User.get_user_by_email(email)

        # Getting staff active status from the Staff object
        status = staffID.active

        # Entering the form data into a model object that will be saved in the database after validation
        user = User(staff = staffID, email = email, password = password)
        
        # Running the validation method on the bottom of the page to see if there are any errors
        error_msg = self.validateUser(staffID, staffemail, status, password, repassword, userCheck)

        # Checking if a error message was returned by the validation
        if not error_msg:
                
                # Hashing the password after not getting any errors from the validation and saving it to the appropriate field in the User object
                user.password = make_password(user.password)
                
                # generating a random string of 8 alphanumeric characters in a loop to get a unique random user ID
                while not error_msg:
                    length = 8
                    ran = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

                    # Checking if generated random ID is unique or not
                    ranCheck = User.get_user_by_ran(ran)
                    if not ranCheck:
                        
                        # Adding the unique random user ID to the appropriate field in the User object
                        user.ran = ran
                        break
                
                # Creating the new user after running all the validations, hashing the password, and generating a random user ID
                user.register()

                # Redirected to the new token generation page
                return redirect('ntoken')
        
        # Rendering the error message and user entered values on the register page after unsuccesful validation
        else:
            data = {
                'error' : error_msg,
                'values' : value,
                }
            return render(request, "register.html", data)
        
        

    # Local method to validate user entered data
    def validateUser(self, staffID, staffemail, status, password, repassword, userCheck):
        error_msg = None
        
        # Password parameter
        pass_upper = any(i.isupper() for i in password)
        pass_lower = any(i.islower() for i in password)
        pass_num = any(i.isnumeric() for i in password)
        pass_special = any(not i.isalnum() for i in password)

        # Checking if staff ID and email fetch the same object from Staff model
        if staffID != staffemail:
            error_msg = "Incorrect Staff ID or Email! Please try again or contact an administrator to get your credentials"
        # Checking if the Staff object has the active status that is needed before registering or generating a token
        elif status != 1:
            error_msg = "You are not authorized to create an account! Please contact an administrator"
        # Applying checks for passworrd length and other password parameters defined above
        elif len(password) <= 7:
            error_msg = "Password is too short! Password must be a combination of 8 uppercase & lowercase letters, numbers, and special characters."    
        elif pass_upper != True:
            error_msg = "There are no uppercase letters in the password! Password must be a combination of 8 upperclass & lowerclass letters, numbers, and special characters."
        elif pass_lower != True:
            error_msg = "There are no lowercase letters in the password! Password must be a combination of 8 upperclass & lowerclass letters, numbers, and special characters."
        elif pass_num != True:
            error_msg = "There are no numbers in the password! Password must be a combination of 8 upperclass & lowerclass letters, numbers, and special characters."
        elif pass_special != True:
            error_msg = "There are no special characters in the password! Password must be a combination of 8 upperclass & lowerclass letters, numbers, and special characters."
        # Checking if entered password matches the re-entered password
        elif password != repassword:
            error_msg = "Password does not match! Please enter the same password again"
        # Checking if a user with the email already exists with the entered email
        elif userCheck:
            error_msg = "User already exists! Please generate a token"

        return error_msg
            
        











    