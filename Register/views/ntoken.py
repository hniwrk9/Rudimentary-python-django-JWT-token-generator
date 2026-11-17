from django.shortcuts import render, redirect
from django.views import View
# Importing django hasher to check the user entered password
from django.contrib.auth.hashers import check_password
# Importing Staff and User model to fetch object for User credential verification and updating Staff status
from Register.models import Staff, User
# Importing the authentication package to create new token or validate an existing token in the session
from Register.jwt import create, validate



class ntoken(View):
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

        return render(request, 'ntoken.html')
    

    def post(self, request):

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

        # Getting form data for verification
        formData = request.POST
        email = formData.get('email')
        password = formData.get('password')

        # Fetching user object against the entered email
        user = User.get_user_by_email(email)
    
        # Checking if there is any user with the email
        if user:
            pass_check = check_password(password, user.password)
            staff = Staff.get_staff_by_csid(user.staff.csid)
            status = staff.active

            # Checking if the staff has the active status needed for token generation
            if status:

                # Checking if password entered by the user is correct
                if pass_check:
                        try:
                            # Getting unique random ID from User object and creating a JWT token with it
                            ntoken = create(user.ran)

                        except:
                            # Rendering the new token page with error message and user entered email if new token creation fails
                            error_msg = "Something went wrong! Please try again or contact an administrator"
                            data = {
                                    'error' : error_msg,
                                    'email' : email,
                            }
                            return render(request, 'ntoken.html', data)

                        # Updating the active status on the Staff object to False and rendering the new JWT token on the frontend to be copied
                        data = {
                            'ntoken' : ntoken,
                        }
                        Staff.updateStatus(user.staff.csid)
                        return render(request, 'token.html', data)
                
                # Creating error message if password check failed
                else:
                    error_msg = "Incorrect credentials! Please try again or contact an administrator"
            
            # Creating error message if staff status is not active for generating tokens
            else:
                error_msg = "You are not authorized to generate a new token! Please contact an administrator"

        # Creating error message if no user found with email
        else:
            error_msg = "Incorrect credentials! Please try again or contact an administrator"

        # Rendering the new token page with the error message and user entered email if credentials were not verified
        data = {
            'error' : error_msg,
            'email' : email,
        }
        return render(request, 'ntoken.html', data)
    


