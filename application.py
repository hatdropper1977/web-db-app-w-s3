#!/usr/bin/env python
import boto3, json, string
from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from models import QuizForm
from random import choice

class Config(object):
    SECRET_KEY = '78w0o5tuuGex5Ktk8VvVDF9Pw3jv1MVE'

S3_BUCKET_NAME = 'transcribe-input-test'

# Generate a random Obkect ID
def random_string_gen(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + '-_'):
    return ''.join(choice(chars) for _ in range(size)) 
s3 = boto3.resource('s3')

application = Flask(__name__)
application.config.from_object(Config)

Bootstrap(application)

@application.route('/', methods=['GET', 'POST'])
def take_test():
    form = QuizForm(request.form)
    if not form.validate_on_submit():
        return render_template('take_quiz_template.html', form=form)
    if request.method == 'POST':
        S3_SUB_BUCKET_NAME = datetime.now().strftime('%Y%m%d')
        S3_OBJECT_NAME = random_string_gen()
        completed_quiz = {}
        completed_quiz['agree'] = request.form.get('agree') 
        completed_quiz['anumber'] = request.form.get('anumber')
        completed_quiz['client_ip_addr'] = request.remote_addr
        completed_quiz['_id'] = S3_OBJECT_NAME
        completed_quiz['ipaddr'] = request.form.get('ipaddr')
        completed_quiz['@timestamp'] = datetime.now().isoformat()
        completed_quiz['textblob'] = request.form.get('textblob')
        S3_OBJECT_JSON = json.dumps(completed_quiz)
        s3 = boto3.resource('s3')
        s3.Object(S3_BUCKET_NAME, '{}/{}.json'.format(S3_SUB_BUCKET_NAME,S3_OBJECT_NAME)).put(Body=S3_OBJECT_JSON)
        return 'Your key is {}/{}.'.format(S3_SUB_BUCKET_NAME,S3_OBJECT_NAME)

@application.route('/user/<user_date>/<user_key>')
def show_user_data(user_date,user_key):
    S3_SUB_BUCKET_NAME = user_date
    S3_OBJECT_NAME = user_key
    obj = s3.Object(S3_BUCKET_NAME, '{}/{}.json'.format(S3_SUB_BUCKET_NAME, S3_OBJECT_NAME))
    user_json = obj.get()['Body'].read().decode('utf-8')
    return render_template( 'show_data_template.html', user_json = json.loads(user_json) )

if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
