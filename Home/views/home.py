from django.shortcuts import render, redirect
from django.views import View
# Importing User model to fetch data after successfully validation
from Register.models import User
# Importing the authentication package for validating the JWT token and decrypting the data
from Register.jwt.validate import validate


class index(View):

    def get(self, request):

        #Checking token in session and redirecting upon failure
        if request.session.get('token'):
            token = request.session.get('token')
            validation = validate(token)
            tokenCheck = validation.get('status')

            #Token validation and redirection upon failure
            if tokenCheck:
                # Rendering Homepage after succesful validation of token
                return render(request, 'index.html')
            
            error_msg = "Invalid Token! Contact an administrator"
            # Deleting invalid token from session and adding error message before redirecting
            del request.session['token']
            request.session['error_msg'] = error_msg
            return redirect('login')
        
        # Adding error message to the session before redirecting
        error_msg = "RESTRICTED ACCESS!!! Log in to access this page!"
        request.session['error_msg'] = error_msg
        return redirect('login')


    def post(self, request):

        #Checking token in session and redirecting upon failure
        if request.session.get('token'):
            token = request.session.get('token')
            validation = validate(token)
            tokenCheck = validation.get('status')

            #Token validation and redirection upon failure
            if tokenCheck:
                # Decrypting the token payload and handling error during decryption
                try:
                    validation = validate(token, data_request=True)

                    # Getting unique random ID after successful decryption
                    rid = validation.get('ran')

                    # Using the decrypted random ID to fetch User object from DB
                    user = User.get_user_by_ran(rid)

                    # The fields below may never be fetched if not necessary. These are only for display purposes
                    csid = user.staff.csid
                    fname = user.staff.fname
                    lname = user.staff.lname
                    email = user.staff.email
                    # The role below should be used to give appropriate access
                    role =  user.staff.role

                    # Sending data to the frontend and rendering it on Index
                    status = validation.get('status')
                    values = {
                        # 'csid': csid,
                        # 'fname': fname,
                        # 'lname': lname,
                        # 'email': email,
                        # 'role': role,
                    }
                    data = {
                        'status': status,
                        'values': values,
                    }
                    return render(request, 'index.html', data)
                
                # Rendering error on frontend upon unsuccessful decryption attempt
                except:
                    error_msg = "There was some error fetching the data! Please contact an administrator!"
                    return render(request, 'index.html', {'error': error_msg})
                
            else:
                error_msg = "Invalid Token! Contact an administrator"
                # Deleting invalid token from session and adding error message before redirecting
                del request.session['token']
                request.session['error_msg'] = error_msg
                return redirect('login')
            
        else:
            # Adding error message to the session before redirecting
            error_msg = "RESTRICTED ACCESS!!! Log in to access this page!"
            request.session['error_msg'] = error_msg
            return redirect('login')


# Simple logout function that delete session on backend to avoid malicious attempt to access the system with a stolen session key
def logout(request):
     request.session.flush()
     return redirect('login')