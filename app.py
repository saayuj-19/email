from flask import Flask, render_template, request, redirect, session, flash
from flask_mail import Mail, Message
import random
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        otp = str(random.randint(100000, 999999))

        session['otp'] = otp
        session['email'] = email
        session['name'] = name

        html = render_template('email_template.html', otp=otp, name=name)
        msg = Message('Your OTP Verification Code', recipients=[email], html=html)
        mail.send(msg)

        return redirect('/verify')

    return render_template('index.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        user_otp = request.form['otp']
        if user_otp == session.get('otp'):
            flash("OTP Verified Successfully!", "success")
        else:
            flash("Invalid OTP. Please try again.", "danger")
    return render_template('verify.html')

if __name__ == '__main__':
    app.run(debug=True)