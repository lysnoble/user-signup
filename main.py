from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def index():
    return render_template('user_validation.html')


@app.route('/validate-user', methods=['POST'])
def validate_user():

    username = request.form['username']
    password = request.form['password']
    verify = request.form['verify']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    validation = True

    if not username or len(username) < 3 or len(username) > 20 or ' ' in username:
        username_error = 'That is not a valid username.'
        username = ''
        validation = False
    
    if not password or len(password) < 3 or len(password) > 20 or ' ' in password:
        password_error = 'That is not a valid password.'
        password = ''
        validation = False

    if not verify or password != verify:
        verify_error = 'The passswords you entered do not match.'
        verify = ''
        validation = False

    if len(email) < 3 and len(email) > 0 or len(email) > 20 or len(email) > 0 and '@' not in email or len(email) > 0 and "." not in email or ' ' in email:
        email_error = 'The email you entered is invalid.'
        email = ''
        validation = False
	
    if validation is False:
        return render_template('user_validation.html', username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error, username=username, password=password, email=email)

    else:
        return render_template('/validated_user.html', username=username)


if __name__ == '__main__':	
    app.run(debug=True)