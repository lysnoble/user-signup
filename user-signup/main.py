from flask import Flask, request, redirect
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def display_form():
    template = jinja_env.get_template('form.html')
    return template.render()

def validate_username(user):
    if user == "":
        return False
    if " " in user:
        return False
    elif len(user) > 20:
        return False
    elif len(user) < 3:
        return False
    else:
        return True

def validate_password(pword):
    if pword == "":
        return False
    if " " in pword:
        return False
    elif len(pword) > 20:
        return False
    elif len(pword) < 3:
        return False
    else:
        return True

def check_password(verify_pword, pword):
    if verify_pword == "":
        return False
    
    if pword != verify_pword:
        return False
    else:
        return True

def validate_email(email):
    if email != "":
        if email.count('@') != 1:
            return False
        if email.count('.') != 1:
            return False
        if " " in email:
            return False
        if len(email) > 20:
            return False
        if len(email) < 3:
            return False
        else:
            return True
    else:
        return True


@app.route('/', methods=['POST'])
def validate():

    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form['email']

    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''

    if not check_password(verify_password, password):
        verify_password_error = "Password and password-confirmation do not match"

    if not validate_password(password):
        password_error = "Not a valid password"

    if not validate_username(username):
        username_error = "Not a valid username"

    if not validate_email(email):
        email_error = "Not a valid email"
        

    if verify_password_error:
        password = ''
        verify_password = ''

    if password_error:
        password = ''
        verify_password = ''

    if username_error:
        username = ''
        password = ''
        verify_password = ''

    if email_error:
        email = ''
        password = ''
        verify_password = ''


    if not username_error and not password_error and not verify_password_error and not email_error:
        user = str(username)
        return redirect('/valid-login?user={0}'.format(user))
    else:
       template = jinja_env.get_template('form.html')
       return template.render(username_error=username_error, password_error=password_error, verify_password_error=verify_password_error,
       email_error=email_error, username=username, password=password, verify_password=verify_password, email=email)


@app.route('/valid-login')
def valid_login():
    user = request.args.get('user')
    welcome = jinja_env.get_template('welcome.html')
    return welcome.render(name=user)

app.run()