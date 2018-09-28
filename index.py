from flask import Flask, request, render_template, json
import os
import pymongo
import pyrebase
import datetime

try:
    from keys import keys
except:
    print("Keys File not Found. Online Access")

API_KEY = os.environ.get('API_KEY') or keys['api_key']
AUTH_DOMAIN = os.environ.get('AUTH_DOMAIN') or keys['auth_domain']
DB_URL = os.environ.get('DB_URL') or keys['db_url']
PROJECT_ID = os.environ.get('PROJECT_ID') or keys['project_id']
STORAGE_BUCKET = os.environ.get('STORAGE_BUCKET') or keys['storage_bucket']
MESSAGING_SENDER_ID = os.environ.get('MESSAGING_SENDER_ID') or keys['messaging_sender_id']
SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT') or keys['service_account']

config = {
  "apiKey": API_KEY,
  "authDomain": AUTH_DOMAIN,
  "databaseURL": DB_URL,
  "projectId": PROJECT_ID,
  "storageBucket": STORAGE_BUCKET,
  "messagingSenderId": MESSAGING_SENDER_ID,
  "serviceAccount": SERVICE_ACCOUNT
}

app = Flask(__name__)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("tester@llov.com", "tester")
db = firebase.database()



@app.route('/')
def index():
    return render_template('main.html', page="Main")


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/dogs', methods = ['POST', 'GET'])
def dogs():
    if request.method == 'POST':
        name = request.form.get('dogName') # TEXT BOX
        gender = request.form['gender'] # RADIO BUTTON
        age = request.form.get('age')
        weight = request.form.get('weight')
        breed = request.form.get('breed')
        comments = request.form.get('comments')
        diseases = request.form.get('diseases')
        dogAggressive = request.form.get('dog-aggressive')
        humanAggressive = request.form.get('human-aggressive')

        data = {
            'Age': int(age),
            'Breed': breed,
            'Gender': gender,
            'Name': name,
            'Weight': int(weight),
            'characteristics':
                {'comments': comments.split(","),
                'diseases': diseases,
                'dog_aggressive': dogAggressive,
                'human_aggressive': humanAggressive},
            'date_added': str(datetime.datetime.now())
        }
        db.child("fosterdogs").push(data)

    dogData = db.child("fosterdogs").get()

    return render_template('fosterdogs.html', data=dogData, page="Foster Dogs")

@app.route('/volunteers', methods = ['POST', 'GET'])
def volunteers():
    if request.method == 'POST':
        print(request.form.get('firstName'))

        name = request.form.get('fullName')  # TEXT BOX
        email = request.form['email']  # RADIO BUTTON
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zip = request.form.get('zipcode')
        number = request.form.get('number')

        # commitment
        volunteering = request.form.get('volunteering')
        Fostering = request.form.get('fostering')
        Adopting = request.form.get('adopting')

        # volunteering
        longterm = request.form.get('long-term-foster')
        shortterm= request.form.get('short-term-foster')
        emergency= request.form.get('emergency-foster')
        coord= request.form.get('coordinating')
        flyers= request.form.get('putting-up-flyers')
        dogwalking= request.form.get('dog-walking')
        fundraising= request.form.get('fundraisers')
        adoptions= request.form.get('helping-at-adoptions')
        transporting= request.form.get('transporting')
        vet = request.form.get('vet-appointments')
        other = request.form.get('volunteering-other')

        # foster_requirements
        female = request.form.get('female')
        male = request.form.get('male')
        small = request.form.get('small')
        large = request.form.get('large')

        breeds = request.form.get('breeds')
        other = request.form.get('fostering-other')

        dogAggressive = request.form.get('dog-aggressive')
        humanAggressive = request.form.get('human-aggressive')

        # data = {
        #     'Age': int(age),
        #     'Breed': breed,
        #     'Gender': gender,
        #     'Name': name,
        #     'Weight': int(weight),
        #     'characteristics':
        #         {'comments': comments.split(","),
        #          'diseases': diseases,
        #          'dog_aggressive': dogAggressive,
        #          'human_aggressive': humanAggressive},
        #     'date_added': str(datetime.datetime.now())
        # }
        # db.child("fosterdogs").push(data)

    return render_template('volunteers.html', page="Volunteers")


@app.route('/fosters', methods = ['POST', 'GET'])
def fosters():
    # pyreObj = db.child("fosters").get().val()
    # data=[]
    # for x, (key, value) in enumerate(pyreObj.items()):
    #     data.append(value)

    if request.method == 'POST':
        name = request.form.get('fosterName')
        street = request.form.get('street')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        canAdoptMore = request.form.get('source')
        humanFriendly = request.form.get('human-friendly')
        dogFriendly = request.form.get('dog-friendly')
        comments = request.form.get('comments')

        data = {
            'Name': name,
            'Address': {
                'Street': street,
                'City': city,
                'State': state,
                'Zipcode': zipcode,
            },
            'canAdoptMore': canAdoptMore,
            'dog_preferences': {
                'dogFriendly': dogFriendly,
                'humanFriendly': humanFriendly,
                'comments': comments
            },
            'timestamp': str(datetime.datetime.now())
        }
        db.child("fosters").push(data)

    fosterData = db.child("fosters").get()
    return render_template('fosters.html', data=fosterData, page="Foster Volunteers")

    # return render_template('fosters.html', data=data, pyreObj=pyreObj, page="Foster Volunteers")


@app.route('/donations', methods = ['POST', 'GET'])
def donationsPage():
    if request.method == 'POST':
        name = request.form.get('donorName')
        amount = request.form.get('amount')
        source = request.form.get('source')
        comments = request.form.get('comments')

        data = {
            'Name': name,
            'amount': amount,
            'comments': comments,
            'source': source,
            'timestamp': str(datetime.datetime.now())
        }
        db.child("donation").push(data)

    donationData = db.child("donation").get()
    return render_template('donations.html', data=donationData, page="Donations")


@app.route('/forms', methods=['GET'])
def formsPage():
    pass


@app.route('/data')
def dataPage():
    return json.jsonify(db.get().val())


@app.route('/onAppLoad')
def onAppLoad():
    pass


if __name__ == '__main__':
    app.run(host='localhost')
