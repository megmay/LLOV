"""
If adding a new route, make sure it belongs here and wouldn't make more sense
    in a controller. If you're making a call to Plaid or FB, a new route
    probably belongs in one of the controllers
    (not applicable if just renaming routes) - MA
"""

from flask import render_template, request
from flask_app import APP
from flask_app import plaid_ctrl, db


@APP.route('/')
@APP.route('/dashboard')
def dashboard():
    """
    description
    """
    data = db.get_dashboard_data()
    return render_template('dashboard.html', page="Dash", data=data)


@APP.route('/login')
def login():
    """
    description

    Going to move the notes below into separate authorization controller - MA
    """
    """
    Act management actions like changing pwd should be in separate route - MA

    if request.form.get('password') == DATA_CHANGE_KEY:
        id = request.form.get('id')[4:]

        if request.form.get('action') == 'delete':
            DB.child(table).child(id).remove()

        elif request.form.get('action') == 'submit':
            get_data, get_keys = data_from(table)
            data = {}
            for key in request.form.keys():
                if key in ('id', 'action', 'password'):
                    continue
                data[key] = request.form.get(key)

            DB.child(table).child(id).set(data)

        else:
            error = True
            error_data = "Password is incorrect"
    """
    return render_template('login.html')


@APP.route('/forms', methods=['GET'])
def get_forms():
    """
    description
    """
    return render_template('forms.html')


@APP.route('/forms', methods=['POST'])
def post_new_form():
    """
    description
    """
    return render_template('create_new_form.html')


@APP.route('/forms/dog', methods=['GET', 'POST'])
def dog_form():
    """
    description
    """

    if request.method == 'POST':
        new_foster_dog_data = {}
        # WTForms needed for this: - MA
        # for field in form:
        #     new_foster_dog_data[field.name] = field.data

        db.add_foster_dog(new_foster_dog_data)

    return render_template('dog_intake_form.html', page="Foster Dog")


@APP.route('/forms/volunteer', methods=['GET', 'POST'])
def volunteer_form():
    """
    description
    """

    if request.method == 'POST':
        new_volunteer_data = {}
        # I want to convert listing the data manually like below
        # to list data automatically like in this for loop: -MA
        # Need to implement WTForms for this - MA
        # for field in form:
        #     new_volunteer_data[field.name] = field.data

        # data = {
        #     'first_name': request.form.get('firstName'),
        #     'last_name': request.form.get('lastName'),
        #     'street': request.form.get('street'),
        #     'city': request.form.get('city'),
        #     'state': request.form.get('state'),
        #     'zipcode': request.form.get('zipcode'),
        #     'phone_number': request.form.get('number'),
        #     'volunteering': {
        #         'can_volunteer': request.form.get('volunteering'),
        #         'longterm': request.form.get('long-term-foster'),
        #         'shortterm': request.form.get('short-term-foster'),
        #         'emergency': request.form.get('emergency-foster'),
        #         'coord': request.form.get('coordinating'),
        #         'flyers': request.form.get('putting-up-flyers'),
        #         'dogwalking': request.form.get('dog-walking'),
        #         'fundraising': request.form.get('fundraisers'),
        #         'adoptions': request.form.get('helping-at-adoptions'),
        #         'transporting': request.form.get('transporting'),
        #         'vet': request.form.get('vet-appointments'),
        #         'other': request.form.get('volunteering-other')
        #     },
        #     'adoption_fostering': {
        #         'can_adopt': request.form.get('adopting'),
        #         'can_foster': request.form.get('fostering'),
        #         'dogTypes': {
        #             'female': request.form.get('female'),
        #             'male': request.form.get('male'),
        #             'small': request.form.get('small'),
        #             'large': request.form.get('large'),
        #             'breeds': request.form.get('breeds'),
        #             'other': request.form.get('fostering-other')
        #         }
        #     }
        # }

        db.add_volunteer(new_volunteer_data)
    return render_template('volunteer_intake_form.html', page="Volunteers")


@APP.route('/forms/foster', methods=['GET', 'POST'])
def foster_form():
    """
    description
    """

    if request.method == 'POST':
        new_foster_data = {}
        # I want to convert listing the data manually like below
        # to list data automatically like in this for loop: - MA
        # Need to implement WTForms for this - MA
        # for field in form:
        #     new_foster_data[field.name] = field.data

        # data = {
        #     'first_name': request.form.get('first_name'),
        #     'last_name': request.form.get('last_name'),
        #     'street': request.form.get('street'),
        #     'city': request.form.get('city'),
        #     'state': request.form.get('state'),
        #     'zipcode': request.form.get('zipcode'),
        #     'can_adopt_more': request.form.get('can_adopt_more'),
        #     'comments': request.form.get('comments'),
        #     'timestamp': str(datetime.datetime.now())
        # }

        db.add_foster(new_foster_data)
    return render_template('foster_volunteer_intake_form.html', page="Fosters")


@APP.route('/forms/donation', methods=['GET', 'POST'])
def donation_form():
    """
    description
    """

    if request.method == 'POST':
        new_donation_data = {}
        # I want to convert listing the data manually like below
        # to list data automatically like in this for loop: - MA
        # Need to implement WTForms for this - MA
        # for field in form:
        #     new_donation_data[field.name] = field.data

        # data = {
        #     'first_name': request.form.get('firstName'),
        #     'last_name': request.form.get('lastName'),
        #     'amount': request.form.get('amount'),
        #     'comments': request.form.get('comments'),
        #     'source': request.form.get('source'),
        #     'timestamp': str(datetime.datetime.now())
        # }
        db.add_donation(new_donation_data)
    return render_template('new_donation_form.html', page="Donations")


@APP.route('/data', methods=['POST', 'GET'])
def get_table_data():
    """
    description

    I like the modular aspect of this method in that it allows
        you to make a general request and depending on the
        contents of that request it will use a different specialized method
        See notes on data_from() in db.py - MA

    However, this needs to be rewritten more cleanly and in the appropriate
        controller file. It also needs to be more descriptive.
        Are you requesting data from Plaid API or Firebase? - MA

    donations, foster volunteers, event volunteers, foster dogs
    """

    data = {}
    table = db.sanitize_user_input(request.args.get('table'))

    if table == "donations" or table is None:
        data = plaid_ctrl.get_plaid_data(request.args.get('request'))

    else:
        data = db.data_from(table, "test")

    return render_template('table_data.html', data=data, page=table)


@APP.route('/update', methods=['POST', 'GET'])
def update():
    """
    description

    Same as above method, needs more description. Whats being updated? - MA
    """
    print(request.args)
    return get_table_data()


@APP.route('/on_app_load')
def on_app_load():
    """
    description

    See above ^  - MA
    """
    pass