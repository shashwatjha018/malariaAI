#External Modules Import
from __future__ import division, print_function
import sys
import os
import glob
import re
import numpy as np
import tensorflow
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, url_for, request, session, redirect, flash, abort
from flask_pymongo import PyMongo
import bcrypt
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired
import email_validator
from flask_mail import Mail, Message
import stripe
import time

#Configuration of our Flask App
app = Flask(__name__)
app.config['SECRET KEY'] = 'Shashwat'

#Database connection  configuration
app.config['MONGO_DBNAME'] = 'Malaria'
app.config['MONGO_URI'] = 'mongodb+srv://Shashwat:shashwat@cluster0.jzqpm.mongodb.net/Malaria1?retryWrites=true&w=majority'

#Mail connection configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = '465'
app.config['MAIL_USERNAME'] = '' #Enter a gmail account
app.config['MAIL_PASSWORD'] = '' #Enter the password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#Stripe connection configuration
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51IoGYzSHuVElli5xKAw6HcMMrSi9hVZ2jPAh5OLbeRd6NXKD98WE5F1udzKjwTkbtXDSL0SKK18qmNe6erNlBeKi00CCMVZyt8'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51IoGYzSHuVElli5xzOpPb0bv0Pjfre4ZiTOcbEiT3cwaQa5lFugN6tNrN4mg1geEGkwnYRAA1NG0TdYRwS5Ix6Y70097DdqvFr'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

mongo = PyMongo(app)
mail = Mail(app)

MODEL_PATH ='cnn_model2.h5'
model = load_model(MODEL_PATH)
def model_predict(file_path,model):
    img = image.load_img(file_path,target_size=(224, 224))
    x = image.img_to_array(img)
    x = x/255
    x = np.expand_dims(x, axis=0)
    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds = "INFECTED"
    else:
        preds = "UNINFECTED"
    return preds


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired(), Length(min=2, max=20)])
    address = StringField('Address', validators = [Length(min=2, max=30)])
    email = StringField('Email', validators = [Email()])
    password = PasswordField('Password', validators = [Length(min=2)])
    confirm_password = PasswordField('Confirm Password', validators = [EqualTo('password')])
    submit = SubmitField('Sign Up & Login')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(min=2)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

@app.route('/', methods = ['GET'])
def landingPage():
    return render_template('landingPage.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    msg = ""
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(f.filename)
        file_path = os.path.join(basepath, 'static/uploads', secure_filename(f.filename))
        f.save(file_path)
        msg = model_predict(file_path,model)
        users = mongo.db.malaria
        login_user = users.find_one({'email' : session['email']})
        users.update_one({'email':login_user['email']},{"$push": {'uploads':{'age':request.form.get('age'),'temperature':request.form.get('temperature'),'file':file_path,'result':msg}}})
        name = login_user['Name']
        age = request.form.get('age')
        temp = request.form.get('temperature')
        flash(f'Upload successful! Check your result','success')
        return render_template("result.html",msg = "Result: "+msg, 
                                filepath = file_path,name = name,age=age,temp=temp)
    elif 'email' in session: 
        users = mongo.db.malaria
        login_user = users.find_one({'email' : session['email']})
        if login_user['payid'] == 'unpaid':
            flash(f'Payment Unsuccesful','danger')   
            return redirect(url_for('pay'))    
        return render_template("features.html") 
    return redirect(url_for('login'))

@app.route('/result', methods = ['GET','POST'])
def result():
    message = Message("Test Result from MalariaAI", sender = "shashwatjha018@gmail.com",recipients=[session['email']])
    message.body = request.form.get('msg')
    mail.send(message)
    flash(f'Result is sent in your mail','success')
    return redirect(url_for('login'))


@app.route('/register',methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        users = mongo.db.malaria
        existing_user = users.find_one({'email' : form.email.data})
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'Name' : form.name.data,'email':form.email.data, 'password' : hashpass,'Address':form.address.data,'status':'unknown','payid':'unpaid'})  #'payment_status':'unpaid'
            session['email'] = form.email.data
            session['status'] = 'unknown'
            flash(f'Account created for {form.name.data}! and successfully logged in','success')
            return redirect(url_for('pay'))
        flash(f'Account already exists!','danger')
        return redirect(url_for('register'))
    return render_template('registration.html', form = form)

@app.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if 'email' in session:
        return render_template('features.html')
    if form.validate_on_submit():
        users = mongo.db.malaria
        login_user = users.find_one({'email' :  form.email.data})
        if login_user:
            if bcrypt.hashpw(form.password.data.encode('utf-8'), login_user['password']) == login_user['password']:
                session['email'] = form.email.data
                session['Name'] = login_user['Name']
                session['status'] = 'unknown'
                if login_user['payid'] == 'unpaid':
                    return redirect(url_for('pay')) 
                return render_template('features.html')
        flash(f'Email or Password is incorrect!','danger')
        return redirect(url_for('login'))
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    form = LoginForm()
    session.pop('email', None)
    session.pop('Name', None)
    flash(f'Successfully logged out','success')
    return redirect(url_for('login'))

#------------------------Stripe Payment--------------------------------
@app.route('/process_pay')
def process_pay():
    time.sleep(6)
    return redirect(url_for('predict'))


@app.route('/pay')
def pay():
    if 'email' in session:
        users = mongo.db.malaria
        pay_user = users.find_one({'email': session['email']})
        print(pay_user['email'])
        if pay_user['payid'] == 'unpaid':
            return render_template('stripe.html')
        flash(f'Already Paid','success')
        return redirect(url_for('predict'))
    return redirect(url_for('login'))       
   
@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1IoTeNSHuVElli5xf1FU3ema',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('process_pay', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('pay', _external=True),
    )
    
    return {
        'checkout_session_id': session['id'], 
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }

      
@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')
    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_cAV9fEA0hm3whG88UP4oPQ6EOGlsJe7X'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']
        print(checkout_session)
        print(checkout_session.payment_status)
        print(checkout_session.payment_intent)
        users = mongo.db.malaria
        pay_user = users.find_one({'email': checkout_session.customer_details.email})
        print(pay_user['email'])
        users.update_one({'email':pay_user['email']},{"$set": {'payid':checkout_session.payment_intent}})
        print(pay_user['payid'])
    return "Success", 200

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)
