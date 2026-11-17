from django.shortcuts import render, redirect
from django.views import View
# Importing the authentication package for validating the JWT token
from Register.jwt.validate import validate



class login(View):

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

        # Checking error messages in session if redirected from a post login page after unsuccessful token validation
        if request.session.get('error_msg'):
            error_msg = request.session.get('error_msg')
            # Deleting error message from session so it doesn't have any unnecessary data
            del request.session['error_msg']
            return render(request, 'login.html', {'error': error_msg,})
        
        # Rendering the login page if the session doesn't have any useful data
        return render(request, 'login.html')


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

        # Getting the token from the login form data after checking the session
        token = request.POST.get('token')
        
        # Validating the token and getting status
        validation = validate(token)
        tokenCheck = validation.get('status')
        
        # Checking validation status
        if not tokenCheck:
            # Getting validation error and displaying on the login page after unsuccessful validation
            error_msg = validation.get('error_msg')
            return render(request, 'login.html', {'error' : error_msg})

        else:
            # Creating session upon successful validation
            request.session['token'] = token
            return redirect('homepage')

